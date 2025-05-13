import sys
from word_games import SpellingBeer

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Arguement Required")

    else:
        letters = sys.argv[1]
        if len(letters) == 7:
            game = SpellingBeer(letters)
            print(game.selected_words)
        else:
            print("Incorrect Number of Letters")
