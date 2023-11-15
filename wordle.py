import random
import random_player
import time


class Wordle:
    def __init__(self):
        self.answers = self.read_answers()
        self.guessable = self.read_guessable()
        self.used_words = set()
        self.n_rounds = 6
        self.responses = ['⬜️', '🟨', '🟩']
        self.answer = None
        self.answer_char_counts = None
        self.all_responses = None

    def read_answers(self):
        with open("answers.txt", "r") as file:
            return file.read().splitlines()

    def read_guessable(self):
        with open("guessable.txt", "r") as file:
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

    def play(self):
        self.all_responses = list()
        self.answer = self.get_random_word()
        self.answer_char_counts = {char: self.answer.count(char) for char in self.answer}

        for i in range (1, self.n_rounds + 1):
            print(f"\nRound {i}")
            while True:
                user_guess = input("Guess: ")
                if user_guess in self.answers or user_guess in self.guessable:
                    break
            
            print(f"Response: {self.evaluate(user_guess)}")
            if user_guess == self.answer:
                self.display_results()
                return
        
        print(f"The word was {self.answer}\n")
        self.display_results()

        self.check_play_again()


    def check_play_again(self):
        repeat = False
        while True:
            repeat_input = input("\nPlay again? y/n: ")
            if repeat_input == 'n':
                return
            elif repeat_input == 'y':
                repeat = True
                break

        if repeat:
            self.play()


    def evaluate(self, guess):
        response = list()
        if self.answer is None or self.all_responses is None:
            print("An error occurred. Cannot evaluate guess.")
            return
        else:
            guess_char_mark_counts = {char: 0 for char in guess}
            for i in range(len(guess)):
                if self.answer[i] == guess[i]:
                    response.append(self.responses[2])
                    guess_char_mark_counts[guess[i]] += 1
                else:
                    response.append(' ')

            for i in range(len(guess)):
                if response[i] == ' ':
                    if guess[i] in self.answer and guess_char_mark_counts[guess[i]] < self.answer_char_counts[guess[i]]:
                        response[i] = self.responses[1]
                        guess_char_mark_counts[guess[i]] += 1
                    else:
                        response[i] = self.responses[0]    

        response_string = ''.join(response)
        self.all_responses.append(response_string)
        return response_string

    def display_results(self):
        print()
        for response in self.all_responses:
            print(response)

    def get_user_choice(self):
        print("\n⬜️🟨🟩 Wordle\n")
        while True: 
            print("1. You play")
            print("2. Random player")
            print("3. AI player")
            print("0. Exit")
            choice = int(input("Select a game mode: "))
            if 0 <= choice <= 3:
                return choice
                

    def play_random(self, show_full_output):
        rp = random_player.RandomPlayer()

        self.all_responses = list()
        self.answer = self.get_random_word()
        self.answer_char_counts = {char: self.answer.count(char) for char in self.answer}

        for i in range (1, self.n_rounds + 1):
            if show_full_output:
                print(f"\nRound {i}")
            while True:
                user_guess = rp.get_next_guess()
                if show_full_output:
                    print(f"Guess: {user_guess}")
                if user_guess in self.answers or user_guess in self.guessable:
                    break
            
            response = self.evaluate(user_guess)

            if show_full_output:
                print(f"Response: {response}")
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
        if(mode == 0):
            return
        elif(mode == 1):
            self.play()
        elif(mode == 2):
            simulation_count = self.get_simulation_count()
            show_full_output = self.get_show_full_output()
            
            win_count = 0
            round_total = 0
            for i in range(1, simulation_count + 1):
                if show_full_output:
                    print(f"\nGame {i}")
                round_won = self.play_random(show_full_output)
                if round_won > 0:
                    round_total += round_won
                    win_count += 1
            
            game_string = "game" if simulation_count == 1 else "games"
            win_string = 'game' if win_count == 1 else 'games'

            print(f"\n{simulation_count} random {game_string}")
            print(f"Win percentage: {'{:.2%}'.format(win_count / simulation_count)} ({win_count} {win_string} won)")
            
            if win_count > 0:
                print(f"Average round of won {win_string}: {'{:.2}'.format(round_total / win_count)}")

            print()



        elif(mode == 3):
            return
        

    def get_simulation_count(self):
        while True:
            count = int(input("\tNumber of games: "))
            if 0 < count <= 1000000:
                return count
    
    def get_show_full_output(self):
        while True:
            show = input("\tShow full output? y/n: ")
            if show == 'n':
                return False
            elif show == 'y':
                return True

wordle = Wordle()
wordle.start()



"""

"""