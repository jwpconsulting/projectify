{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/23.11";
    poetry2nix = {
      url = "github:nix-community/poetry2nix/2023.12.2614813";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
# see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryEnv defaultPoetryOverrides;
        projectDir = self;
        overrides = defaultPoetryOverrides.extend (self: super: {
          django-cloudinary-storage = super.django-cloudinary-storage.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
            });
          django-pgconnection = super.django-pgconnection.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.poetry ];
            });
          twisted = super.twisted.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling super.hatch-fancy-pypi-readme ];
            });
          django-pgtrigger = super.django-pgtrigger.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.poetry ];
            });
        });
      in
      {
        devShell = mkPoetryEnv {
          inherit projectDir;
          inherit overrides;
        };
      });
}
