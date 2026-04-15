# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024-2026 JWP Consulting GK
{
  description = "Projectify Nix flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";

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
          # Copy with:
          htmx-js = pkgs.stdenv.mkDerivation rec {
            pname = "htmx-js";
            version = src.rev;
            src = pkgs.fetchFromGitHub {
              owner = "bigskysoftware";
              repo = "htmx";
              rev = "v2.0.8";
              sha256 = "sha256-hHBX3UkxRJTULzGsunUFQBYYrAKqmVdAHwj9LoCjTlg=";
            };
            installPhase = ''
              mkdir $out
              cp src/htmx.js $out/htmx.js
            '';
          };

          # cp $(nix build .#htmx-js --print-out-paths --no-link)/htmx.js projectify/static/htmx.js
          htmx-bundle = pkgs.stdenv.mkDerivation {
            pname = "htmx-bundle";
            version = htmx-js.version;
            dontUnpack = true;
            buildInputs = [ htmx-js ];
            installPhase = ''
              mkdir $out
              echo "\
              /*! SPDX-License-Identifier: 0BSD
                  SPDX-FileCopyrightText: NONE */" > $out/htmx.js
              cat ${htmx-js}/htmx.js  >> $out/htmx.js
            '';
          };
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

            # Deployment
            pkgs.ansible
          ];
        };
      }
    );
}
