with import <nixpkgs> { };

let myPython3 =
  python3.withPackages(ps: with ps; [
    python3Packages.ipdb
    python3Packages.ipdbplugin
    python3Packages.ipython
    python3Packages.unidecode
    python3Packages.nose
    # python3Packages.PySMT
    python3Packages.z3
  ])
;
in stdenv.mkDerivation rec {
  name = "smt-playground-env";

  buildInputs = [
    myPython3
  ];
}

