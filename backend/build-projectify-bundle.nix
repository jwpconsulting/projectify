# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
{ nodejs
, python312Packages
, python312
, postgresql_15

, tailwind-deps

, poetry2nix
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
    django-browser-reload = [ "setuptools" ];
  };
  overrides = poetry2nix.defaultPoetryOverrides.extend
    (self: super: {
      # poetry2nix is being sunset. instead fixing the build for the
      # following packages, I'm just including the ones from nixos instead
      # Since these are transient dependencies, I don't believe we'll
      # be affected too much by changes within them.
      # Justus 2024-12-25
      constantly = python312Packages.constantly;
      cffi = python312Packages.cffi;
      pyyaml = python312Packages.pyyaml;
      # Fix this error:
      # error: builder for '/nix/store/5bvgc1n6nim0khffcny1yy9d8fy96i87-python3.12-urllib3-2.6.0.drv' failed with exit code 1;
      #        last 25 log lines:
      #        >       self.metadata.validate_fields()
      #        >     File "/nix/store/fbbghklswdr1r7czsnrcyh41ssri6cp4-python3.12-hatchling-1.27.0/lib/python3.12/site-packages/hatchling/metadata/core.py", line 266, in validate_fields
      #        >       self.core.validate_fields()
      #        >     File "/nix/store/fbbghklswdr1r7czsnrcyh41ssri6cp4-python3.12-hatchling-1.27.0/lib/python3.12/site-packages/hatchling/metadata/core.py", line 1366, in validate_fields
      #        >       getattr(self, attribute)
      #        >     File "/nix/store/fbbghklswdr1r7czsnrcyh41ssri6cp4-python3.12-hatchling-1.27.0/lib/python3.12/site-packages/hatchling/metadata/core.py", line 991, in classifiers
      #        >       raise ValueError(message)
      #        >   ValueError: Unknown classifier in field `project.classifiers`: Programming Language :: Python :: Free Threading :: 2 - Beta
      urllib3 = super.urllib3.overridePythonAttrs (
        old: {
          # By passing in HATCH_METADATA_CLASSIFIERS_NO_VERIFY = "yes"
          # https://github.com/pypa/hatch/pull/1620
          # > Add a HATCH_METADATA_CLASSIFIERS_NO_VERIFY hook to disable
          # verification of trove classifiers. This makes it possible to build
          # newer packages against old versions of trove-classifiers (or even
          # without the package installed). This is a convenience feature for
          # Linux distributions that do not want to track minimum required
          # trove-classifiers versions as required by various packages.
          HATCH_METADATA_CLASSIFIERS_NO_VERIFY = "yes";
        }
      );
      psycopg-c = super.psycopg-c.overridePythonAttrs (
        old: {
          nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [
            postgresql_15
            # >   running dist_info
            # >   creating /build/pip-modern-metadata-jinlj1xa/psycopg_c.egg-info
            # >   writing /build/pip-modern-metadata-jinlj1xa/psycopg_c.egg-info/PKG-INFO
            # >   writing dependency_links to /build/pip-modern-metadata-jinlj1xa/psycopg_c.egg-info/dependency_links.txt
            # >   writing top-level names to /build/pip-modern-metadata-jinlj1xa/psycopg_c.egg-info/top_level.txt
            # >   writing manifest file '/build/pip-modern-metadata-jinlj1xa/psycopg_c.egg-info/SOURCES.txt'
            # >   couldn't run 'pg_config' --includedir: [Errno 2] No such file or directory: 'pg_config'
            # >   error: [Errno 2] No such file or directory: 'pg_config'
            postgresql_15.pg_config
          ];
          buildInputs = (old.buildInputs or [ ]) ++ [
            super.setuptools
            super.tomli
          ];
        }
      );
      cryptography = python312Packages.cryptography;
      # This refuses to build because Poetry can't deal with the syntax
      # of project.license in markdown's pyproject.toml file
      markdown = python312Packages.markdown;
      # substituteStream() in derivation python3.12-pillow-10.3.0: ERROR: pattern AVIF_ROOT\ =\ None doesn't match anything in file 'setup.py'
      pillow = python312Packages.pillow;
    } // (builtins.mapAttrs
      # Thanks to
      # https://github.com/nix-community/poetry2nix/blob/master/docs/edgecases.md#modulenotfounderror-no-module-named-packagename
      (package: build-requirements: (
        (builtins.getAttr package super).overridePythonAttrs (old: {
          buildInputs = (old.buildInputs or [ ]) ++ (builtins.map (pkg: if builtins.isString pkg then builtins.getAttr pkg super else pkg) build-requirements);
        })
      ))
      pypkgs-build-requirements));
in
# see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
  # https://github.com/nix-community/poetry2nix?tab=readme-ov-file#mkpoetryapplication
(poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  inherit overrides;
  python = python312;
  buildInputs = [ nodejs ];
  groups = [ "main" ];
  checkGroups = [ ];
  outputs = [ "out" "static" ];
  preConfigure = ''
    mkdir projectify/theme/static projectify/theme/static/css
    cp -r ${tailwind-deps}/dist projectify/theme/static/css/dist
  '';
  postInstall = ''
    mkdir $out/{bin,etc}
    cp manage.py "$out/bin"

    cp gunicorn.conf.py gunicorn-error.log $out/etc/

    mkdir $static
    env \
      DJANGO_SETTINGS_MODULE=projectify.settings.collect_static \
      DJANGO_CONFIGURATION=CollectStatic \
      STATIC_ROOT=$static \
      python $out/bin/manage.py collectstatic --no-input
  '';
}).overrideAttrs (super: {
  passthru = super.passthru // {
    postgresql = postgresql_15;
  };
})
