let
  # Niv
  sources = import ./nix/sources.nix;
  pkgs = import sources.nixpkgs { };
  inherit (pkgs.lib) optional optionals;
  # Python
  python-env = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
  };
in pkgs.mkShell {
  buildInputs = [
    python-env
    pkgs.poetry
    pkgs.sqlite
  ];

}
