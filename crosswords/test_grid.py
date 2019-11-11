import nose

from functools import reduce

from grid import Grid, Word


class TestWord:
    def setUp(self):
        self.wordlist = [ Word((0, 0), 4, 'h')
                        , Word((1, 0), 4, 'h')
                        , Word((2, 0), 4, 'h')
                        , Word((0, 1), 4, 'v')
                        , Word((1, 1), 4, 'v')
                        , Word((2, 1), 4, 'v')
                        ]


    def test_can_be_seen_has_a_variable_name(self):
        results = list(map(
            lambda w: w.as_variable_name,
            self.wordlist
        ))

        expected_results = [ 'h_0_0'
                           , 'h_1_0'
                           , 'h_2_0'
                           , 'v_0_1'
                           , 'v_1_1'
                           , 'v_2_1'
                           ]

        nose.tools.assert_list_equal(results, expected_results)


    def test_line_index(self):
        results = list(map(
            lambda w: w.line_index,
            self.wordlist
        ))

        expected_results = [ 0, 1, 2, 0, 1, 2 ]

        nose.tools.assert_list_equal(results, expected_results)


    def test_column_index(self):
        results = list(map(
            lambda w: w.column_index,
            self.wordlist
        ))

        expected_results = [ 0, 0, 0, 1, 1, 1 ]

        nose.tools.assert_list_equal(results, expected_results)



class TestGrid:
    def setUp(self):
        self.grid = Grid([ [ '1', '0', '1', '1' ]
                         , [ '0', '0', '0', '0' ]
                         , [ '1', '0', '0', '0' ]
                         , [ '0', '0', '1', '0' ]
                         , [ '1', '0', '0', '0' ]
                         , [ '1', '0', '0', '0' ]
                         , [ '1', '0', '0', '0' ]
                         ])

    def _format_word(self, w):
        return (w.position, w.length, w.direction)

    def test_extract_words_from_frame(self):
        results = list(map(
            self._format_word,
            self.grid.words
        ))

        expected_results = [ ( (1, 0), 4, 'h' )
                           , ( (2, 1), 3, 'h' )
                           , ( (3, 0), 2, 'h' )
                           , ( (4, 1), 3, 'h' )
                           , ( (5, 1), 3, 'h' )
                           , ( (6, 1), 3, 'h' )
                           , ( (0, 1), 7, 'v' )
                           , ( (1, 2), 2, 'v' )
                           , ( (4, 2), 3, 'v' )
                           , ( (1, 3), 6, 'v' )
                           ]

        nose.tools.assert_list_equal(results, expected_results)


    def test_can_list_all_words_of_a_column(self):
        results = list(map(
            self._format_word,
            reduce(
                lambda acc, j: acc + self.grid.words_on_column(j),
                [ 0, 1, 2, 3 ],
                []
            )
        ))

        expected_results = [ ( (0, 1), 7, 'v' )
                           , ( (1, 2), 2, 'v' )
                           , ( (4, 2), 3, 'v' )
                           , ( (1, 3), 6, 'v' )
                           ]

        nose.tools.assert_list_equal(results, expected_results)


    def test_can_give_a_list_of_crossing_word_with_their_intersection_position(self):
        results = sorted(list(map(
            lambda x: ( self._format_word(x[0]), self._format_word(x[1]), x[2] ),
            self.grid.words_crossing_with_intersection
        )))

        expected_results = [ ( ((1, 0), 4, 'h'), ((0, 1), 7, 'v'), (1, 1) )
                           , ( ((1, 0), 4, 'h'), ((1, 2), 2, 'v'), (1, 2) )
                           , ( ((1, 0), 4, 'h'), ((1, 3), 6, 'v'), (1, 3) )

                           , ( ((2, 1), 3, 'h'), ((0, 1), 7, 'v'), (2, 1) )
                           , ( ((2, 1), 3, 'h'), ((1, 2), 2, 'v'), (2, 2) )
                           , ( ((2, 1), 3, 'h'), ((1, 3), 6, 'v'), (2, 3) )

                           , ( ((3, 0), 2, 'h'), ((0, 1), 7, 'v'), (3, 1) )

                           , ( ((4, 1), 3, 'h'), ((0, 1), 7, 'v'), (4, 1) )
                           , ( ((4, 1), 3, 'h'), ((1, 3), 6, 'v'), (4, 3) )
                           , ( ((4, 1), 3, 'h'), ((4, 2), 3, 'v'), (4, 2) )

                           , ( ((5, 1), 3, 'h'), ((0, 1), 7, 'v'), (5, 1) )
                           , ( ((5, 1), 3, 'h'), ((1, 3), 6, 'v'), (5, 3) )
                           , ( ((5, 1), 3, 'h'), ((4, 2), 3, 'v'), (5, 2) )

                           , ( ((6, 1), 3, 'h'), ((0, 1), 7, 'v'), (6, 1) )
                           , ( ((6, 1), 3, 'h'), ((1, 3), 6, 'v'), (6, 3) )
                           , ( ((6, 1), 3, 'h'), ((4, 2), 3, 'v'), (6, 2) )
                           ]

        nose.tools.assert_list_equal(results, expected_results)
