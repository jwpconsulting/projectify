# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
{
  description = "Flake file for Projectify backend";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";

    flake-utils.url = "github:numtide/flake-utils";

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
        python = pkgs.python312;
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
          djlint = [ "hatchling" ];
          django-tailwind = [ "poetry" ];
          selectolax = [ "setuptools" ];
          django-components = [ "setuptools" ];
          django-browser-reload = [ "setuptools" ];
        };
        overrides = defaultPoetryOverrides.extend (self: super: {
          # poetry2nix is being sunset. instead fixing the build for the
          # following packages, I'm just including the ones from nixos instead
          # Since these are transient dependencies, I don't believe we'll
          # be affected too much by changes within them.
          # Justus 2024-12-25
          constantly = pkgs.python312Packages.constantly;
          cffi = pkgs.python312Packages.cffi;
          pyyaml = pkgs.python312Packages.pyyaml;
          psycopg-c = super.psycopg-c.overridePythonAttrs (
            old: {
              nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [
                postgresql
                # >   running dist_info
                # >   creating /build/pip-modern-metadata-jinlj1xa/psycopg_c.egg-info
                # >   writing /build/pip-modern-metadata-jinlj1xa/psycopg_c.egg-info/PKG-INFO
                # >   writing dependency_links to /build/pip-modern-metadata-jinlj1xa/psycopg_c.egg-info/dependency_links.txt
                # >   writing top-level names to /build/pip-modern-metadata-jinlj1xa/psycopg_c.egg-info/top_level.txt
                # >   writing manifest file '/build/pip-modern-metadata-jinlj1xa/psycopg_c.egg-info/SOURCES.txt'
                # >   couldn't run 'pg_config' --includedir: [Errno 2] No such file or directory: 'pg_config'
                # >   error: [Errno 2] No such file or directory: 'pg_config'
                postgresql.pg_config
              ];
              buildInputs = (old.buildInputs or [ ]) ++ [
                super.setuptools
                super.tomli
              ];
            }
          );
          cryptography = pkgs.python312Packages.cryptography;
          # This refuses to build because Poetry can't deal with the syntax
          # of project.license in markdown's pyproject.toml file
          markdown = pkgs.python312Packages.markdown;
          # substituteStream() in derivation python3.12-pillow-10.3.0: ERROR: pattern AVIF_ROOT\ =\ None doesn't match anything in file 'setup.py'
          pillow = pkgs.python312Packages.pillow;
        } // (builtins.mapAttrs
          (package: build-requirements: (
            (builtins.getAttr package super).overridePythonAttrs (old: {
              buildInputs = (old.buildInputs or [ ]) ++ (builtins.map (pkg: if builtins.isString pkg then builtins.getAttr pkg super else pkg) build-requirements);
            })
          ))
          pypkgs-build-requirements));
        tailwind-deps = pkgs.buildNpmPackage {
          name = "tailwind-deps";
          src = ./.;
          npmDeps = pkgs.importNpmLock {
            npmRoot = ./projectify/theme/static_src;
          };
          buildInputs = [ pkgs.nodejs ];
          preConfigure = ''
            cd projectify/theme/static_src
          '';
          installPhase = ''
            mkdir -p $out
            cp ../static/css/dist/styles.css $out/styles.css
          '';
          npmConfigHook = pkgs.importNpmLock.npmConfigHook;
        };
        # https://github.com/nix-community/poetry2nix?tab=readme-ov-file#mkpoetryapplication
        projectify-bundle = mkPoetryApplication {
          inherit projectDir;
          inherit overrides;
          inherit python;
          buildInputs = [ pkgs.nodejs ];
          groups = [ "main" ];
          checkGroups = [ ];
          outputs = [ "out" "static" ];
          preConfigure = ''
            mkdir -p projectify/theme/static/css
            cp ${tailwind-deps}/styles.css projectify/theme/static/css
          '';
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
        devShell = pkgs.mkShell {
          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ postgresql ];
          buildInputs = [
            postgresql
            postgresql.pg_config
            pkgs.nodejs
            pkgs.heroku
            pkgs.openssl
            pkgs.gettext
          ];
        };
      });
}
