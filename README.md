# SMT solvers playground

  * [Crosswords](crosswords/solve.py): Generate crossword grids.
  * [Sudoku](sudoku.py): Generate valid Sudoku grids.
    Alternatively, can be used to solve Sudoku grids by adding a couple of well-chosen constraints...
  * [Planning](planning/solve.py): Create a planning, depending on people's availabilities, and respecting some "business requirements".


## Environment

```
nix-shell -p 'python37.withPackages(ps: with ps; [ unidecode PySMT z3 ])'
```

For `PySMT`, see [Pamplemousse/nixpkgs's `angr` branch](https://github.com/Pamplemousse/nixpkgs/tree/angr).
