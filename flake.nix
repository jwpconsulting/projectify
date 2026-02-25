# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
{
  description = "Projectify app Nix flake";

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
        pkgs = nixpkgs.legacyPackages.${system};
        projectify-bundle = pkgs.callPackage ./build-projectify-bundle.nix {
          poetry2nix = poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
        };
      in
      {
        packages = rec {
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
        };
        devShell = pkgs.mkShell {
          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ projectify-bundle.passthru.postgresql ];
          buildInputs = [

            # TODO I temporarily commented out these build inputs. Are they
            # still needed?
            # backend
            # manage

            # Run things locally
            pkgs.librsvg

            # Docs
            pkgs.nodePackages.prettier

            # For backend development
            projectify-bundle.passthru.postgresql
            projectify-bundle.passthru.postgresql.pg_config
            pkgs.openssl
            pkgs.gettext
            pkgs.stripe-cli

            # License
            pkgs.reuse
          ];
        };
      });
}
