'''
NOTE FROM THE AUTHOR: I'm tired of these games.
TODO:
    - HANDLE UPPER/LOWER CASE
    - CHECK FOR SYMBOLS (SEE mêlée, élan, flambé, etc.)
'''

import numpy as np


''' This is the super class for the words games. Let the user use at their own risk.
'''
class WordListManipulator():

    '''
    --------------------------------------------------------------------------------
    input:
    - filepath: String containing the path to a dictionary that should be used
    --------------------------------------------------------------------------------
    '''
    def __init__(self, filepath='/usr/share/dict/words'):
        with open(filepath) as word_dict:
            self.words = word_dict.read().splitlines()
        self.selected_words = self.words.copy()
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    '''
    --------------------------------------------------------------------------------
    trims the 'selected length' member to words of selected length
    --------------------------------------------------------------------------------
    inputs:
    - n: desired length
    - remove_words_with_apostrophes: removes words that contain an apostraphe
    - remove_proper_nouns: removes words that have a capital first letter
    - keep_n_or_greater: keeps words of n or greater instead of exactly n
    --------------------------------------------------------------------------------
    '''
    def keep_words_of_length_n(self, n, remove_words_with_apostrophes=True, remove_proper_nouns=True, remove_symbols=True, keep_n_or_greater=False):
        if keep_n_or_greater:
            self.selected_words = [word for word in self.selected_words if len(word) >= n]
        else:
            self.selected_words = [word for word in self.selected_words if len(word) == n]
        if remove_words_with_apostrophes:
            self.selected_words = [word for word in self.selected_words if '\'' not in word]
        if remove_proper_nouns:
            self.selected_words = [word for word in self.selected_words if word.islower()]
        if remove_symbols:
            self.selected_words = [word for word in self.selected_words if word.isalpha()]

    '''
    --------------------------------------------------------------------------------
    removes all words with a particular letter
    --------------------------------------------------------------------------------
    inputs:
    - l: selected letter
    --------------------------------------------------------------------------------
    '''
    def remove_words_with_letter(self, l):
        self.selected_words = [word for word in self.selected_words if not l in word]

    '''
    --------------------------------------------------------------------------------
    removes all words without a particular letter
    --------------------------------------------------------------------------------
    inputs:
    - l: selected letter
    --------------------------------------------------------------------------------
    '''
    def remove_words_without_letter(self, l):
        self.selected_words = [word for word in self.selected_words if l in word]

    '''
    --------------------------------------------------------------------------------
    returns words from self.selected_words that include the selected letter
    --------------------------------------------------------------------------------
    inputs:
    - l: selected letter
    --------------------------------------------------------------------------------
    '''
    def get_words_with_letter(self, l):
        return [word for word in self.selected_words if l in word]

    '''
    --------------------------------------------------------------------------------
    returns the number of unique letters in a string
    --------------------------------------------------------------------------------
    inputs:
    - word: selected string
    --------------------------------------------------------------------------------
    '''
    def count_unique_letters(self, word):
        return len(set(word))

    '''
    --------------------------------------------------------------------------------
    sorts self.selected_words by the number of unique letter, from low to high
    --------------------------------------------------------------------------------
    '''
    def sort_by_unique_letters(self):
        self.selected_words = sorted(self.selected_words, key=lambda word: self.count_unique_letters(word))

    '''
    --------------------------------------------------------------------------------
    returns words selected by the user
    --------------------------------------------------------------------------------
    '''
    def get_selected_words(self):
        return self.selected_words.copy()

    '''
    --------------------------------------------------------------------------------
    returns the selected_words member to include the full set
    --------------------------------------------------------------------------------
    '''
    def start_over(self):
        self.selected_words = self.words.copy()


''' This class is specifically useful for the game Wordle.
'''
class Wordler(WordListManipulator):

    def __init__(self, filepath='/usr/share/dict/words'):
        super().__init__(filepath)
        self.keep_words_of_length_n(5)
        self.words = self.selected_words.copy()

    def remove_words_without_letter_in_index(self, l, index):
        self.selected_words = [word for word in self.selected_words if word[index] == l]

    def remove_words_with_letter_in_index(self, l, index):
        self.selected_words = [word for word in self.selected_words if not word[index] == l]


''' This class is specifically useful for the game Spelling Bee.
'''
class SpellingBeer(WordListManipulator):

    # TODO: CORRECT LOGIC SO IT DOESN'T SEARCH THE LIST 19 TIMES, BUT ONE TIME
    def __init__(self, center_letter, l1=None, l2=None, l3=None, l4=None, l5=None, l6=None, filepath='/usr/share/dict/words'):
        super().__init__(filepath)
        self.keep_words_of_length_n(4, keep_n_or_greater=True)
        # TODO: ADDRESS WRONG NUMBER OF LETTERS
        if len(center_letter) == 1:
            self.remove_words_without_letter(center_letter)
            self.available_letters = [center_letter, l1, l2, l3, l4, l5, l6]
        elif len(center_letter) == 7:
            self.remove_words_without_letter(center_letter[0])
            self.available_letters = []
            for l in center_letter:
                self.available_letters.append(l)
        to_remove = [l for l in self.alphabet if l not in self.available_letters]
        for letter in to_remove:
            self.remove_words_with_letter(letter)
        self.words = self.selected_words.copy()

    def get_words_using_all_letters(self):
        words_ = self.selected_words.copy()
        for letter in self.available_letters:
            words_ = [word for word in words_ if letter in word]
        return words_


''' This class is specifically useful for the game Letter Boxed.
'''
class LetterBoxer(WordListManipulator):

    '''
    inputs:
    - four_walls: the four walls of the box, ex. [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j', 'k', 'l'], ['m', 'n', 'o', 'p']]
    '''
    def __init__(self, four_walls, filepath='/usr/share/dict/words'):
        # initialize
        super().__init__(filepath)
        self.keep_words_of_length_n(3, keep_n_or_greater=True)
        # remove words that contain an unavailable letter
        four_walls_np = np.array(four_walls).flatten()
        to_remove = [l for l in self.alphabet if l not in four_walls_np]
        for letter in to_remove:
            self.remove_words_with_letter(letter)
        # remove words with double letters
        for wall in four_walls:
            for l1 in wall:
                for l2 in wall:
                    self.remove_words_with_substring(l1 + l2)
        # set master list equal to subgroup
        self.sort_by_unique_letters()
        self.words = self.selected_words.copy()

        self.two_word_solutions = []
        self.check_for_pair_completion()

    '''
    --------------------------------------------------------------------------------
    checks for two-word pairs that complete the puzzle, beginning with the words
    with the most unique letters
    --------------------------------------------------------------------------------
    '''
    def check_for_pair_completion(self):
        for big_word in reversed(self.words):
            lefts = self.get_words_ending_with_letter(big_word[0])
            for left in lefts:
                if self.count_unique_letters(left + big_word) == 12 and (left + " " + big_word) not in self.two_word_solutions:
                    self.two_word_solutions.append(left + " " + big_word)
                    # print(left + " " + big_word)
                    # return # comment out to print all two-word combinations
            rights = self.get_words_beginning_with_letter(big_word[-1])
            for right in rights:
                if self.count_unique_letters(big_word + right) == 12 and (big_word + " " + right) not in self.two_word_solutions:
                    # print(big_word + " " + right)
                    # return # comment out to print all two-word combinations
                    self.two_word_solutions.append(big_word + " " + right)

    '''
    --------------------------------------------------------------------------------
    removes the words with a particular substring from self.selected_words
    --------------------------------------------------------------------------------
    inputs:
    - ss: particular substring
    --------------------------------------------------------------------------------
    '''
    def remove_words_with_substring(self, ss):
        self.selected_words = [word for word in self.selected_words if ss not in word]

    '''
    --------------------------------------------------------------------------------
    returns the words beginning with a particular letter from self.selected_words
    --------------------------------------------------------------------------------
    inputs:
    - l: particular letter
    --------------------------------------------------------------------------------
    '''
    def get_words_beginning_with_letter(self, l):
        return [word for word in self.selected_words if word[0] == l]

    '''
    --------------------------------------------------------------------------------
    returns the words ending with a particular letter from self.selected_words
    --------------------------------------------------------------------------------
    inputs:
    - l: particular letter
    --------------------------------------------------------------------------------
    '''
    def get_words_ending_with_letter(self, l):
        return [word for word in self.selected_words if word[-1] == l]


if __name__ == '__main__':

    a = Wordler()
    a.remove_words_without_letter_in_index('o', 1)
    a.remove_words_without_letter_in_index('d', 4)
    a.remove_words_without_letter('p')
    a.remove_words_with_letter_in_index('p', 2)
    # print(a.get_selected_words())

    b = SpellingBeer('c', 'e', 'h', 'l', 'o', 's', 'u')
    # print(b.get_selected_words())
    # print(b.get_words_using_all_letters())

    # walls = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['j', 'k', 'l']]
    walls = [['i', 'u', 'r'], ['w', 'h', 'n'], ['e', 'a', 'p'], ['x', 'm', 'o']]
    c = LetterBoxer(walls)
    c.sort_by_unique_letters()
    print(c.get_words_with_letter('x'))
    # print(c.get_words_ending_with_letter('p'))
    print(c.get_words_ending_with_letter('e'))
    print(c.get_words_beginning_with_letter('r'))
    # print(c.selected_words)
