# SMT solvers playground

  * [Sudoku](sudoku.py): Generate valid Sudoku grids.
    Alternatively, can be used to solve Sudoku grids by adding a couple of well-chosen constraints...


## Environment

```
nix-shell -p 'python37.withPackages(ps: with ps; [ PySMT z3 ])'
```

For `PySMT`, see [Pamplemousse/nixpkgs's `angr` branch](https://github.com/Pamplemousse/nixpkgs/tree/angr).
