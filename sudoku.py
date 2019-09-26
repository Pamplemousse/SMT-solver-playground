import itertools

from functools import reduce

from pysmt.shortcuts import And, Equals, GE, get_model, Int, is_sat, LT, Not, Plus, Symbol
from pysmt.typing import INT


GRID = [[ Symbol("%d_%d" % (i, j), INT) for j in range(1, 10) ] for i in range(1, 10) ]

def all_distincts(values):
    return And(reduce(
        lambda acc, i: acc + [ Not(Equals(values[i], values[j])) for j in range(i+1, len(values)) ],
        range(len(values)),
        []
    ))

def get_3x3_bloc(offsets):
    i_offset = offsets[0]
    j_offset = offsets[1]
    return reduce(
        lambda acc, i: acc + [ GRID[i_offset + i][j_offset + j] for j in range(3) ],
        range(3),
        []
    )


cells_are_digits = And(reduce(
    lambda acc, line: acc + [ And(GE(cell, Int(1)), LT(cell, Int(10))) for cell in line ],
    GRID,
    []
))

each_line_has_no_duplicates = And(list(map(
    lambda line: all_distincts(line),
    GRID
)))

each_column_has_no_duplicates = And(list(map(
    lambda j: all_distincts([ line[j] for line in GRID ]),
    range(9)
)))

each_3x3_bloc_has_no_duplicates = And(list(map(
    lambda offsets: all_distincts(get_3x3_bloc(offsets)),
    itertools.product(range(0, 9, 3), range(0, 9, 3))
)))


formula = And(
    cells_are_digits,
    each_line_has_no_duplicates,
    each_column_has_no_duplicates,
    each_3x3_bloc_has_no_duplicates,
)

model = get_model(formula)
if model:
    results = map(
        lambda line: [ model[cell] for cell in line ],
        GRID
    )

    # Print the results line by line for a nice grid look.
    list(map(
        print,
        results
    ))
else:
    print("No solution found")
