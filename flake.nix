# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024-2026 JWP Consulting GK
{
  description = "Projectify Nix flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        postgres = pkgs.postgresql_15;
      in
      {
        packages = rec {
          # This is where projectify-bundle once lived
        };
        devShell = pkgs.mkShell {
          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ postgres ];
          buildInputs = [
            # Favicon generation
            pkgs.librsvg

            # Docs
            pkgs.nodePackages.prettier

            # For backend development
            postgres
            postgres.pg_config
            pkgs.openssl
            pkgs.gettext
            pkgs.stripe-cli
          ];
        };
      }
    );
}
