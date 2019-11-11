import time
from functools import reduce

from z3 import And, is_eq, Length, Or, sat, Solver, String, StringVal

from dictionary import sorted_wordlist as DICTIONARY
from grid import GRID


GUESSES = list(map(
    lambda x: (String(x[0]), x[1]),
    map(
        lambda word: (word.as_variable_name, word.length),
        GRID.words,
    )
))


def are_words_from(guesses, wordlist):
    """
    :param List[Tuple[Z3.String,Int]] guesses:
    :param Dict[Int,List[String]] wordlist:
    """
    def is_word(guess, length):
        return Or([ (guess == word) for word in wordlist[length] ])

    return And(list(map(
        lambda g: is_word(*g),
        guesses
    )))


def all_distincts(guesses):
    """
    :param List[Tuple[Z3.String,Int]] guesses:
    """
    return And(reduce(
        lambda acc, i: acc + [ guesses[i][0] != guesses[j][0] for j in range(i+1, len(guesses)) ],
        range(len(guesses)),
        []
    ))


def crossing_points(grid):
    def _have_letter_in_common(word1, word2, intersection_point):
        position1 = intersection_point[1] - word1.column_index
        position2 = intersection_point[0] - word2.line_index

        variable_word1 = String(word1.as_variable_name)
        variable_word2 = String(word2.as_variable_name)

        return variable_word1[position1] == variable_word2[position2]

    return And(list(map(
        lambda x: _have_letter_in_common(*x),
        grid.words_crossing_with_intersection
    )))


formula = And([
    are_words_from(GUESSES, DICTIONARY),
    all_distincts(GUESSES),
    crossing_points(GRID)
])



print('Formula is ready!')

solver = Solver()
second = 1000
minute = 60 * second
hour = 60 * minute
solver.set('timeout', 100 * hour)
solver.add(formula)

start = time.clock()
is_formula_sat = solver.check()
end = time.clock()

print('Formula is %s, in %f seconds' % (is_formula_sat, end - start))

if is_formula_sat == sat:
    model = solver.model()

    print(model)
else:
    print("No solution found")

import ipdb; ipdb.set_trace()
