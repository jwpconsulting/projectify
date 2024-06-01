# TODO
# - Make mypy etc available from inside poetry env
{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/23.11";
    poetry2nix = {
      url = "github:nix-community/poetry2nix/master";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication mkPoetryEnv defaultPoetryOverrides;
        projectDir = self;
        postgresql = pkgs.postgresql_15;
        python = pkgs.python311;
        # Thanks to
        # https://github.com/nix-community/poetry2nix/blob/master/docs/edgecases.md#modulenotfounderror-no-module-named-packagename
        pypkgs-build-requirements = {
          django-anymail = [ "hatchling" ];
          django-cloudinary-storage = [ "setuptools" ];
          django-debug-toolbar = [ "hatchling" "setuptools" ];
          django-pgtrigger = [ "poetry" ];
          django-ratelimit = [ "setuptools" ];
          django-test-migrations = [ "poetry" ];
          editables = [ "flit-core" ];
          sqlparse = [ "hatchling" ];
          twisted = [ "hatchling" "hatch-fancy-pypi-readme" ];
          types-stripe = [ "setuptools" ];
        };
        overrides = defaultPoetryOverrides.extend (self: super: {
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
          cryptography = super.cryptography.overridePythonAttrs (old: rec {
            cargoDeps = pkgs.rustPlatform.fetchCargoTarball {
              inherit (old) src;
              name = "${old.pname}-${old.version}";
              sourceRoot = "${old.pname}-${old.version}/${cargoRoot}";
              sha256 = "sha256-qaXQiF1xZvv4sNIiR2cb5TfD7oNiYdvUwcm37nh2P2M=";
            };
            cargoRoot = "src/rust";
          });
        } // (builtins.mapAttrs
          (package: build-requirements: (
            (builtins.getAttr package super).overridePythonAttrs (old: {
              buildInputs = (old.buildInputs or [ ]) ++ (builtins.map (pkg: if builtins.isString pkg then builtins.getAttr pkg super else pkg) build-requirements);
            })
          ))
          pypkgs-build-requirements));
        poetryEnv = mkPoetryEnv {
          inherit projectDir;
          inherit overrides;
          inherit python;
          pyproject = ./pyproject.toml;
          poetrylock = ./poetry.lock;
          groups = [ "dev" "test" ];
        };
        projectify-backend = mkPoetryApplication {
          inherit projectDir;
          inherit overrides;
          inherit python;
          pyproject = ./pyproject.toml;
          poetrylock = ./poetry.lock;
          groups = [ ];
          buildInputs = [ pkgs.makeWrapper ];
          outputs = [ "out" "static" ];
          # The DATABASE_URL below will only work on localhost
          postInstall = ''
            cp \
              manage.py \
              "$out/bin"
            mkdir "$static"
            DJANGO_SETTINGS_MODULE=projectify.settings.development \
              DJANGO_CONFIGURATION=DevelopmentNix \
              STATIC_ROOT="$static" \
              python "$out/bin/manage.py" collectstatic \
                --no-input
            wrapProgram "$out/bin/manage.py" \
              --set DJANGO_SETTINGS_MODULE projectify.settings.development \
              --set DJANGO_CONFIGURATION DevelopmentNix \
              --set DATABASE_URL postgres://%2Fvar%2Frun%2Fpostgresql/projectify \
              --set STATIC_ROOT "$static"
            wrapProgram "$out/bin/projectify-backend" \
              --set DJANGO_SETTINGS_MODULE projectify.settings.development \
              --set DJANGO_CONFIGURATION DevelopmentNix \
              --set PORT 8000 \
              --set STATIC_ROOT "$static" \
              --set DATABASE_URL postgres://%2Fvar%2Frun%2Fpostgresql/projectify \
              --add-flags --config \
              --add-flags ${./gunicorn.conf.py} \
              --add-flags --log-config \
              --add-flags ${./gunicorn-error.log}
          '';
        };
      in
      {
        packages = {
          inherit projectify-backend;
          default = projectify-backend;
          container = pkgs.dockerTools.buildLayeredImage {
            name = "projectify-backend";
            tag = "latest";
            contents = [ projectify-backend pkgs.bash pkgs.coreutils pkgs.file ];
            # For /var/run/postgresql
            extraCommands = ''
              mkdir -p var/run/postgresql
            '';
            config = {
              Cmd = [ "${projectify-backend}/bin/projectify-backend" ];
              ExposedPorts = {
                "8000/tcp" = {};
              };
              Volumes = {
                "/var/run/postgresql" = {};
              };
            };
          };
        };
        # Run with `nix run`
        apps = {
          default = {
            type = "app";
            program = "${projectify-backend}/bin/projectify-backend";
          };
        };
        devShell = poetryEnv.env.overrideAttrs (oldattrs: {
          buildInputs = [
            postgresql
            pkgs.heroku
            pkgs.openssl
          ];
        });
      });
}
