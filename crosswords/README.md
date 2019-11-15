# Crossword grids generation

I posted a series of articles, detailing the construction of this solution, on my blog:
  * [Introduction to SMT, and programming with SMT Solvers (currently reading)](https://blog.xaviermaso.com/2019/11/11/Use-SMT-Solvers-to-generate-crossword-grids-(1).html)
  * [Definitions and first formulas](https://blog.xaviermaso.com/2019/11/12/Use-SMT-Solvers-to-generate-crossword-grids-(2).html)
  * [Plumbing everything together, complete formula, and results](https://blog.xaviermaso.com/2019/11/13/Use-SMT-Solvers-to-generate-crossword-grids-(3).html)


## Folder content

  * `francais.txt`: The wordlist where the words are chosen from;
  * `generate_dictionary.py`: A script to generate this "normalised" wordlist (remove diacritics, deduplicate) out of a French wordlist found online;
  * `dictionary.py`: The representation of the wordlist as a Python structure, with the logic of "splitting" it into several pieces per the word size, as detailed [in the second post](https://blog.xaviermaso.com/2019/11/12/Use-SMT-Solvers-to-generate-crossword-grids-(2).html#a-single-valid-word).
  * `grid.py`: The scanning of a grid from `0`s and `1`s, and interface to query grid related content, such as: list of words and intersections, with their coordinates, following the convention [exposed in the third post](https://blog.xaviermaso.com/2019/11/13/Use-SMT-Solvers-to-generate-crossword-grids-(3)#variables).
  * `test_grid.py`: Some unit test for the above logic;
  * `solve.py`: **The central piece**, making use of the above components to generate the formula as exposed in the series, call the solver, and print a solution (~~ when ~~ if found).
