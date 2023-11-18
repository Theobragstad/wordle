class AIPlayer:
    def __init__(self):
        self.guessable_words = self.get_guessable_words()

    def get_guessable_words(self):
        with open("answers.txt", "r") as answers_file, open("guessable.txt", "r") as guessable_file:
            answers = answers_file.read().splitlines()
            guessable = guessable_file.read().splitlines()

        return answers + guessable
    
    def get_next_guess(self):
        return "hello"
