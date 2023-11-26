import random

class RandomPlayer:
    def __init__(self):
        self.guessable = self.get_guessable_words()

    def get_guessable_words(self):
        with open("all_words.txt", "r") as file:
            return file.read().splitlines()
    
    def get_guess(self):
        guess = random.choice(self.guessable)
        if guess in self.guessable:
            self.guessable.remove(guess)
        
        return guess