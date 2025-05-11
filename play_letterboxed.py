import sys
from word_games import LetterBoxer

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Arguement Required")

    else:
        letters = sys.argv[1]
        if len(letters) == 12:
            four_walls = []
            for ii in range(4):
                wall = []
                for jj in range(3):
                    wall.append(str(letters[3*ii + jj]))
                four_walls.append(wall)
            game = LetterBoxer(four_walls)
            if len(game.two_word_solutions) > 0:
                print(game.two_word_solutions)
            else:
                print("No Two-Word Solutions")
        else:
            print("Incorrect Number of Letters")
