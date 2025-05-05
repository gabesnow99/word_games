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
            print(game.two_word_solutions[0])
        else:
            print("Incorrect Number of Letters")