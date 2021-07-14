let
  # Niv
  sources = import ./nix/sources.nix;
  pkgs = import sources.nixpkgs { };
  unstable = import <nixos-unstable> {config = {allowUnfree=true;};};
  inherit (pkgs.lib) optional optionals;
  # Python
  python-env = unstable.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    python = unstable.python37;
  };
in pkgs.mkShell {
  buildInputs = [
    python-env
    unstable.python37Packages.pip
    unstable.python37Packages.bandit
    unstable.python37Packages.pep8
    unstable.python37Packages.flake8
    unstable.python37Packages.autopep8
    pkgs.poetry
    pkgs.sqlite
    pkgs.docker
  ];

}
