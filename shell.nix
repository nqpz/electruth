with import <nixpkgs> {};

mkShell {
  buildInputs = [
    (python3.withPackages (ps: with ps; [ termcolor setproctitle ]))
    geda
  ];
}
