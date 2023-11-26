import random
import time

import random_player


class Wordle:
    def __init__(self):
        self.answers = self.read_answers()
        self.guessable = self.read_guessable()
        self.used_words = set()
        self.n_rounds = 6
        self.answer = None
        self.answer_char_counts = None
        self.all_responses = None
        self.grayLetters = []
        self.yellowLetters = []
        self.greenLetters = []
        self.all_guesses = []

    def read_answers(self):
        with open("answer_words.txt", "r") as file:
            return file.read().splitlines()

    def read_guessable(self):
        with open("all_words.txt", "r") as file:
            return file.read().splitlines()

    def get_random_word(self):
        available_words = list(set(self.answers) - self.used_words)

        if not available_words:
            print("(All words used. Resetting word bank.)")
            self.used_words = set()
            available_words = list(set(self.answers) - self.used_words)

        word = random.choice(available_words)
        self.used_words.add(word)
        return word

    def display_letters(self):
        if len(self.grayLetters) > 0:
            print("⬜️", *self.grayLetters, sep=" ")
        
        if len(self.yellowLetters) > 0:
            print("🟨", *self.yellowLetters, sep=" ")

        if len(self.greenLetters) > 0:
            print("🟩", *self.greenLetters, sep=" ")
            
    def play_normal(self):
        self.grayLetters = []
        self.yellowLetters = []
        self.greenLetters = []
        self.all_guesses = []
        self.all_responses = list()
        self.answer = self.get_random_word()
        self.answer_char_counts = {
            char: self.answer.count(char) for char in self.answer
        }

        for i in range(1, self.n_rounds + 1):
            print(f"\nRound {i}")
            if i > 1:
                self.display_current_board()
            try:
                while True:
                    user_guess = input("Guess: ")
                    if user_guess in self.guessable:
                        break
                self.all_guesses.append(user_guess)
                self.evaluate(user_guess)
                if user_guess == self.answer:
                    print(f"\nYou won in {i} round{'s' if i > 1 else ''}.")
                    self.display_results()
                    self.save_results()
                    self.check_play_again()
                    return
            except KeyboardInterrupt:
                return

        print(f"\nYou lost.")
        print(f"The word was {self.answer}")
        self.display_results()
        self.save_results()
        self.check_play_again()

    def count_wins(self):
        count = 0
        with open('wordle_results.txt', 'r') as file:
            for line in file:
                count += line.count('🟩🟩🟩🟩🟩')
        return count
    
    def get_num_wordles_played(self):
        with open('wordle_results.txt', 'r') as file:
            content = file.read()

        latest_wordle_number = None
        for line in reversed(content.split('\n')):
            if line.startswith('wordle '):
                latest_wordle_number = int(line.split(' ')[-1])
                break
        return latest_wordle_number
    
    def save_results(self):
        existing_wordle_numbers = []
        try:
            with open('wordle_results.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith('wordle'):
                        try:
                            wordle_number = int(line.split()[1])
                            existing_wordle_numbers.append(wordle_number)
                        except (ValueError, IndexError):
                            pass

        except FileNotFoundError:
            pass

        if existing_wordle_numbers:
            wordle_number = max(existing_wordle_numbers) + 1
        else:
            wordle_number = 1

        with open('wordle_results.txt', 'a+') as file:
            file.write(f'wordle {wordle_number}\n')

            for response in self.all_responses:
                file.write(response + '\n')
            file.write("\n")
        self.update_stats(self.count_wins(), round((self.count_wins() / self.get_num_wordles_played()) * 100, 1), self.get_avg_win_round())



    def get_avg_win_round(self):
        sum_indexes = 0
        win_count = 0

        with open('wordle_results.txt', 'r') as file:
            lines = file.readlines()

        i = 0
        while i < len(lines):
            line = lines[i]

            if "wordle " in line and not line.startswith("wordle results"):
                startIndex = 1
                for j in range(i + 1, min(i + 7, len(lines))):
                    if "🟩🟩🟩🟩🟩" in lines[j]:
                        sum_indexes += startIndex
                        win_count += 1
                        break
                    startIndex += 1
               
            i += 1  

        return 0 if win_count == 0 else round((sum_indexes / win_count), 1)





    def update_stats(self, win_count, win_percentage, average_win_round):
        try:
            with open('wordle_results.txt', 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            lines = []

        stats_present = any(line.startswith('wordle results') for line in lines)

        with open('wordle_results.txt', 'w') as file:
            if stats_present:
                for i, line in enumerate(lines):
                    if line.startswith('win count:'):
                        lines[i] = f'win count: {win_count}\n'
                    elif line.startswith('win percentage:'):
                        lines[i] = f'win percentage: {win_percentage}\n'
                    elif line.startswith('average win round:'):
                        lines[i] = f'average win round: {average_win_round}\n'
            else:
                file.write(f'wordle results \n\n')
                file.write(f'win count: {win_count}\n')
                file.write(f'win percentage: {win_percentage}\n')
                file.write(f'average win round: {average_win_round}\n\n')

            file.writelines(lines)


    def show_green_letters_helper(self):
        helper = ""
        for letter in self.answer:
            if letter in self.greenLetters:
                helper += letter
            else :
                helper += " _ "

        if helper[0] == " ":
            helper = helper[1:]

        if not all(letter == "_" for letter in helper.replace(" ", "")):
            print(f"\n{helper}\n")

    def check_play_again(self):
        repeat = False
        while True:
            repeat_input = input("Play again? y/n: ")
            if repeat_input == "n":
                return
            elif repeat_input == "y":
                repeat = True
                break

        if repeat:
            self.play_normal()

    def evaluate(self, guess):
        response = list()
        if self.answer is None or self.all_responses is None:
            print("An error occurred. Cannot evaluate guess.")
            return
        else:
            guess_char_mark_counts = {char: 0 for char in guess}
            for i in range(len(guess)):
                if self.answer[i] == guess[i]:
                    response.append("🟩")
                    guess_char_mark_counts[guess[i]] += 1
                   
                    if guess[i] not in self.greenLetters:
                            self.greenLetters.append(guess[i])

                    for letter in self.grayLetters:
                        if letter == guess[i]:
                            self.grayLetters.remove(letter)
                    for letter in self.yellowLetters:
                        if letter == guess[i]:
                            self.yellowLetters.remove(letter)
                else:
                    response.append(" ")

            for i in range(len(guess)):
                if response[i] == " ":
                    if (
                        guess[i] in self.answer
                        and guess_char_mark_counts[guess[i]]
                        < self.answer_char_counts[guess[i]]
                    ):
                        response[i] = "🟨"
                        guess_char_mark_counts[guess[i]] += 1
                        
                        if guess[i] not in self.yellowLetters:
                            self.yellowLetters.append(guess[i])

                        for letter in self.grayLetters:
                            if letter == guess[i]:
                                self.grayLetters.remove(letter)
                        for letter in self.greenLetters:
                            if letter == guess[i]:
                                self.greenLetters.remove(letter)
                    
                    else:
                        response[i] = "⬜️"
                        if guess[i] not in self.grayLetters:
                            self.grayLetters.append(guess[i])

                        for letter in self.yellowLetters:
                            if letter == guess[i]:
                                self.yellowLetters.remove(letter)
                        for letter in self.greenLetters:
                            if letter == guess[i]:
                                self.greenLetters.remove(letter)
                        
        
     


        response_string = "".join(response)
        self.all_responses.append(response_string)
        return response_string

    def display_current_board(self):
        print()
        for i in range(len(self.all_guesses)):
            print(" ".join(self.all_guesses[i]))
            print(self.all_responses[i])
        print()

    def display_results(self):
        print()
        for response in self.all_responses:
            print(response)
        print()

    def get_user_choice(self):
        print("\n⬜️🟨🟩 wordle\n")
        print("1. You play")
        print("2. Random player")
        print("3. AI player (Minimax)")
        print("4. AI player (Alpha-beta)")
        print("0. Exit")
        while True:
            try:
                choice = int(input("Select a game mode: "))
                if 0 <= choice <= 4:
                    return choice
                
            except ValueError:
                pass

            except KeyboardInterrupt:
                return


    def play_mode(self, mode, show_full_output):
        if mode == 2:
            player = random_player.RandomPlayer()
        elif mode == 3:
            pass
        elif mode == 4:
            pass

        self.all_responses = list()
        self.answer = self.get_random_word()
        self.answer_char_counts = {
            char: self.answer.count(char) for char in self.answer
        }

        for i in range(1, self.n_rounds + 1):
            if show_full_output:
                print(f"\nRound {i}")
            while True:
                user_guess = player.get_guess()
                if show_full_output:
                    print(f"Guess: {user_guess}")
                if user_guess in self.guessable:
                    break

            response = self.evaluate(user_guess)

            if show_full_output:
                print(response)
            if user_guess == self.answer:
                self.display_results()
                time.sleep(1.5)
                return i

        if show_full_output:
            print(f"The word was {self.answer}\n")

        self.display_results()

        return 0

    def start(self):
        mode = self.get_user_choice()
        if mode == 0:
            return
        elif mode == 1:
            self.play_normal()
        elif mode == 2:
            self.mode(2)
        elif mode == 3:
            pass
        elif mode == 4:
            pass

    def mode(self, mode):
        simulation_count = self.get_simulation_count()
        show_full_output = self.get_show_full_output()

        if mode == 2:
            print("\nStarting random player...")
        elif mode == 3:
            print("\nStarting AI player (Minimax)...")
        elif mode == 4:
            print("\nStarting AI player (Alpha-beta)...")

        time.sleep(1.5)

        win_count = 0
        round_total = 0
        for i in range(1, simulation_count + 1):
            if show_full_output:
                print(f"\nGame {i}")

            if mode == 2:
                round_won = self.play_mode(2, show_full_output)
            if mode == 3:
                round_won = self.play_mode(3, show_full_output)
            if mode == 4:
                round_won = self.play_mode(4, show_full_output)

            if round_won > 0:
                round_total += round_won
                win_count += 1

        game_string = "game" if simulation_count == 1 else "games"
        win_string = "game" if win_count == 1 else "games"

        print(f"\n{simulation_count} random {game_string}")
        print(
            f"Win percentage: {'{:.4%}'.format(win_count / simulation_count)} ({win_count} {win_string} won)"
        )
        if win_count > 0:
            print(
                f"Average round of won {win_string}: {'{:.4}'.format(round_total / win_count)}"
            )

        print()

    def get_simulation_count(self):
        try:
            while True:
                count = int(input("\tNumber of games: "))
                if 0 < count <= 100000:
                    return count
        except KeyboardInterrupt:
            return

    def get_show_full_output(self):
        try:
            while True:
                show = input("\tShow full output? y/n: ")
                if show == "n":
                    return False
                elif show == "y":
                    return True
        except KeyboardInterrupt:
            return


wordle = Wordle()
wordle.start()