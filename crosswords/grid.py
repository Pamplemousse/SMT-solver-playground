import re

from functools import partial, reduce


# frame of http://frv100.com/fleches/mf001.htm
# 1 - definitions
# 0 - blank cell
# GRID_FRAME = [
#     [ '1', '0', '1', '0', '1', '0', '1', '0', '1', '0', '1' ,'0' ],
#     [ '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0' ,'0' ],
#     [ '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0' ,'0' ],
#     [ '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0' ,'0' ],
#     [ '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0' ,'0' ],
#     [ '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0' ,'1' ],
#     [ '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0' ,'0' ],
#     [ '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0' ,'0' ],
#     [ '1', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1' ,'0' ],
#     [ '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0' ,'0' ],
#     [ '1', '0', '0', '0', '0', '0', '1', '0', '0', '1', '0' ,'0' ],
#     [ '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0' ,'0' ],
#     [ '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1' ,'0' ],
#     [ '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0' ,'0' ],
#     [ '1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0' ,'1' ],
#     [ '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0' ,'0' ],
#     [ '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0' ,'0' ],
#     [ '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0' ,'0' ],
# ]
GRID_FRAME = [
    [ '1', '0', '1', '0', '1', '0' ],
    [ '0', '0', '0', '0', '0', '0' ],
    [ '1', '0', '0', '0', '0', '0' ],
    [ '0', '0', '0', '0', '0', '0' ],
    [ '1', '0', '0', '0', '0', '1' ],
    [ '0', '0', '0', '0', '1', '0' ],
    [ '1', '0', '0', '0', '0', '0' ],
    [ '0', '0', '0', '1', '0', '0' ],
    [ '1', '0', '1', '0', '0', '0' ],
    [ '0', '0', '0', '0', '0', '0' ],
    [ '1', '0', '0', '0', '0', '0' ],
    [ '0', '0', '0', '0', '1', '0' ],
]
# GRID_FRAME = [
#     [ '1', '0', '1' ],
#     [ '0', '0', '0' ],
#     [ '1', '0', '0' ],
#     [ '0', '0', '0' ],
#     [ '1', '0', '0' ],
#     [ '0', '0', '0' ],
# ]


class Word:
    def __init__(self, position, length, direction):
        """
        :param Tuple(int, int) position:
            A couple of coordinates indicating the position of the first character of the word on the grid.
        :param int length: The number of characters that the word contains.
        :param char direction: 'h' for an horizontal word or 'v' for a vertical word.
        """
        assert direction == 'v' or direction == 'h', ("Direction should be 'h' or 'v', not %s" % direction)

        self.position = position
        self.length = length
        self.direction = direction

    @property
    def as_variable_name(self):
        return "%s_%s_%s" % (self.direction, self.position[0], self.position[1])

    @property
    def line_index(self):
        return self.position[0]

    @property
    def column_index(self):
        return self.position[1]


def _lines_as_strings(grid_frame):
    return list(map(
        lambda l: ''.join(l),
        grid_frame
    ))

def _columns_as_strings(grid_frame):
    column_length = len(grid_frame[0])
    columns = map(
        lambda j: [ line[j] for line in grid_frame ],
        range(column_length)
    )
    return list(map(
        lambda c: ''.join(c),
        columns
    ))

def _words_for_line(line_number, line_content):
    return list(map(
        lambda r: Word((line_number, r.start()), len(r.group()), 'h'),
        re.finditer(r"0{2}0*", line_content)
    ))

def _words_for_column(column_number, column_content):
        return list(map(
            lambda r: Word((r.start(), column_number), len(r.group()), 'v'),
            re.finditer(r"0{2}0*", column_content)
        ))


class Grid:
    def __init__(self, frame):
        """
        :param Array[Array[Int]] frame:
            The representation of the grid using a matrix where: 1 stands for a definition slot, 0 for an empty cell.
        """
        self._horizontal_words = reduce(
            lambda acc, line: acc + _words_for_line(*line),
            enumerate(_lines_as_strings(frame)),
            []
        )
        self._vertical_words = reduce(
            lambda acc, column: acc + _words_for_column(*column),
            enumerate(_columns_as_strings(frame)),
            []
        )

        self.words = self._horizontal_words + self._vertical_words

    def words_on_column(self, j):
        return list(filter(
            lambda w: w.column_index == j,
            self._vertical_words
        ))

    @property
    def words_crossing_with_intersection(self):
        def _in_range(word, candidate):
            if candidate.line_index <= word.line_index and (candidate.line_index + candidate.length - 1) >= word.line_index:
                return (word.line_index, candidate.column_index)
            else:
                return None

        def _words_crossing_with_intersection(word):
            candidates = reduce(
                lambda acc, j: acc + self.words_on_column(j),
                range(word.column_index, word.column_index + word.length),
                []
            )

            _in_range_of_word = partial(_in_range, word)

            return list(filter(
                lambda x: x[2] is not None,
                map(
                    lambda c: (word, c, _in_range_of_word(c)),
                    candidates
                ))
            )

        words = reduce(
            lambda acc, w: acc + _words_crossing_with_intersection(w),
            self._horizontal_words,
            []
        )

        return words


GRID = Grid(GRID_FRAME)
