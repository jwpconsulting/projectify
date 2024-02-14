# TODO
# - Make mypy etc available from inside poetry env
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
        postgresql = pkgs.postgresql_15;
        python = pkgs.python311;
        overrides = defaultPoetryOverrides.extend (self: super: {
          django-cloudinary-storage = super.django-cloudinary-storage.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
            }
          );
          twisted = super.twisted.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling super.hatch-fancy-pypi-readme ];
            }
          );
          django-pgtrigger = super.django-pgtrigger.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.poetry ];
            }
          );
          psycopg-c = super.psycopg-c.overridePythonAttrs (
            old: {
              nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [
                postgresql
              ];
              buildInputs = (old.buildInputs or [ ]) ++ [
                super.setuptools
                super.tomli
              ];
            }
          );
          django-test-migrations = super.django-test-migrations.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.poetry ];
            }
          );
          types-stripe = super.types-stripe.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
            }
          );
          editables = super.editables.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.flit-core ];
            }
          );
          django-debug-toolbar = super.django-debug-toolbar.overridePythonAttrs (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling super.setuptools ];
            }
          );
        });
        poetryEnv = mkPoetryEnv {
          inherit projectDir;
          inherit overrides;
          inherit python;
          pyproject = ./pyproject.toml;
          poetrylock = ./poetry.lock;
          groups = [ "dev" "test" ];
        };
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            python
            poetryEnv
            postgresql
            pkgs.heroku
            # Allow poetry to install
            pkgs.openssl
          ];
          shellHook = ''
            # For gunicorn
            export PORT=8000
          '';
        };
      });
}
