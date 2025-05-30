{ mkPoetryApplication
, nodejs
, python3Packages
, python
, defaultPoetryOverrides
, postgresql
, tailwind-deps
}:
let
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
  overrides = defaultPoetryOverrides.extend
    (self: super: {
      # poetry2nix is being sunset. instead fixing the build for the
      # following packages, I'm just including the ones from nixos instead
      # Since these are transient dependencies, I don't believe we'll
      # be affected too much by changes within them.
      # Justus 2024-12-25
      constantly = python3Packages.constantly;
      cffi = python3Packages.cffi;
      pyyaml = python3Packages.pyyaml;
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
      cryptography = python3Packages.cryptography;
      # This refuses to build because Poetry can't deal with the syntax
      # of project.license in markdown's pyproject.toml file
      markdown = python3Packages.markdown;
      # substituteStream() in derivation python3.12-pillow-10.3.0: ERROR: pattern AVIF_ROOT\ =\ None doesn't match anything in file 'setup.py'
      pillow = python3Packages.pillow;
    } // (builtins.mapAttrs
      (package: build-requirements: (
        (builtins.getAttr package super).overridePythonAttrs (old: {
          buildInputs = (old.buildInputs or [ ]) ++ (builtins.map (pkg: if builtins.isString pkg then builtins.getAttr pkg super else pkg) build-requirements);
        })
      ))
      pypkgs-build-requirements));
in
mkPoetryApplication {
  projectDir = ./.;
  inherit overrides;
  inherit python;
  buildInputs = [ nodejs ];
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
}
