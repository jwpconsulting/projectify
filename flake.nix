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
          trix-js = pkgs.stdenv.mkDerivation rec {
            pname = "trix";
            version = "2.1.18";
            src = pkgs.fetchFromGitHub {
              owner = "basecamp";
              repo = "trix";
              rev = "v${version}";
              sha256 = "sha256-fyyXJiYCho031P1Ni9ehDdUk8smPqMZnayWvZXPoHaM=";
            };
            offlineCache = pkgs.fetchYarnDeps {
              yarnLock = "${src}/yarn.lock";
              sha256 = "sha256-8ihDdBuk2VliY+l2bAySzg7uDdMitwx9QFuEUL/disM=";
            };
            nativeBuildInputs = [
              pkgs.yarnConfigHook
              pkgs.nodejs
              pkgs.rake
            ];
            # This fixes a /usr/bin/env issue, and
            # changes lines like the following to use url() instead:
            # $icon-attach: svg('trix/images/attach.svg');
            # becomes
            # $icon-attach: url('./attach.svg');
            postPatch = ''
              patchShebangs --build bin/sass-build
              sed -i "s|svg('trix|url('.|g" assets/trix/stylesheets/icons.scss
            '';
            buildPhase = ''
              export HOME=$(mktemp -d)
              yarn --offline build
            '';
            installPhase = ''
              mkdir $out $out/images
              echo "\
/*! SPDX-License-Identifier: MIT
    SPDX-FileCopyrightText: 37signals, LLC */" > $out/trix.umd.js
              cat dist/trix.umd.js >> $out/trix.umd.js
              echo "\
/*! SPDX-License-Identifier: MIT
    SPDX-FileCopyrightText: 37signals, LLC */" > $out/trix.css
              cat dist/trix.css >> $out/trix.css
              cp -a assets/trix/images/*.svg $out/images
            '';
          };

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
