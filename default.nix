with import <nixpkgs> {};
stdenv.mkDerivation {
    name = "electruth";
    buildInputs = [ (python3.withPackages (ps: with ps; [ termcolor setproctitle ])) ];
}
