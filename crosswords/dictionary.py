from functools import reduce
from random import shuffle

from z3 import StringVal


DICTIONARY_PATH = 'crosswords/francais.txt'

MIN_WORD_SIZE = 2
MAX_WORD_SIZE = 18

def keep_only_words_of_good_length(wordlist):
    return list(filter(
        lambda word: len(word) >= MIN_WORD_SIZE and len(word) <= MAX_WORD_SIZE,
        wordlist
    ))

def update_dict(python_dict, key, value):
    python_dict.update({ key: value })
    return python_dict


wordlist = open(DICTIONARY_PATH, 'r').read().split('\n')
wordlist = keep_only_words_of_good_length(wordlist)

# Let `dictionary` be a dict, where keys an int, and values the list of words of length "key", as Z3 String variables.
def _update_wordlist(acc, word):
    key = len(word)
    current_value = acc[len(word)]
    new_value = current_value + [ StringVal(word) ]

    acc.update({ key: new_value })
    return acc

sorted_wordlist = reduce(
    _update_wordlist,
    wordlist,
    { length: [] for length in range(MIN_WORD_SIZE, MAX_WORD_SIZE + 1) }
)

# For when the Solver is crumbling under the weight of the formula that is sent:
# Let's reduce the search space by making the wordlists smaller.
# Also, shuffle not to have only words starting with the letter 'a'.
# for word_length, wordlist in sorted_wordlist.items():
#     shuffle(wordlist)
#     sorted_wordlist[word_length] = wordlist[:500]
