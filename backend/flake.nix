{
  description = "Flake file for Projectify backend";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
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
        projectDir = ./.;
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
          groups = [ "dev" "test" ];
        };
        projectify-bundle = mkPoetryApplication {
          inherit projectDir;
          inherit overrides;
          inherit python;
          groups = [ ];
          checkGroups = [ ];
          outputs = [ "out" "static" ];
          postInstall = ''
            mkdir -p $out/bin $out/etc
            cp manage.py "$out/bin"

            cp gunicorn.conf.py gunicorn-error.log $out/etc/

            mkdir -p $static
            env \
              DJANGO_SETTINGS_MODULE=projectify.settings.collect_static \
              DJANGO_CONFIGURATION=CollectStatic \
              STATIC_ROOT=$static \
              python $out/bin/manage.py collectstatic --no-input
          '';
          # Disable checking runtime dependencies
          # https://github.com/nix-community/poetry2nix/issues/1441
          dontCheckRuntimeDeps = true;
        };
      in
      {
        packages = {
          # Expose projectify-bundle for caching
          inherit projectify-bundle;
          projectify-manage = pkgs.writeShellApplication {
            name = "projectify-manage";
            runtimeInputs = [ projectify-bundle.dependencyEnv ];
            # TODO consider whether STATIC_ROOT is reallse needed to run a
            # management comma
            text = ''
              export STATIC_ROOT="${projectify-bundle.static}"
              exec ${projectify-bundle}/bin/manage.py "$@"
            '';
          };
          projectify-backend = pkgs.writeShellApplication {
            name = "projectify-backend";
            runtimeInputs = [ projectify-bundle.dependencyEnv ];
            text = ''
              export STATIC_ROOT="${projectify-bundle.static}"
              exec gunicorn --config ${projectify-bundle}/etc/gunicorn.conf.py --log-config ${projectify-bundle}/etc/gunicorn-error.log --access-logfile -
            '';
          };
          projectify-celery = pkgs.writeShellApplication {
            name = "projectify-celery";
            runtimeInputs = [ projectify-bundle.dependencyEnv ];
            # TODO make worker independent of STATIC_ROOT
            text = ''
              export STATIC_ROOT="${projectify-bundle.static}"
              exec celery --app projectify.celery worker --concurrency 1
            '';
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
