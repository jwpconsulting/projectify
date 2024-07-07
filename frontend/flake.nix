# SPDX-License-Identifier: AGPL-3.0-or-later
# Nix Flakes file
# Copyright (C) 2024 JWP Consulting GK

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
{
  description = "Projectify frontend";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        nodejs = pkgs.nodejs_20;
        mkFrontend = {
            wsEndpoint ? "/ws"
            , apiEndpoint ? "/api"
            , projectifyDomain ? "https://www.projectify.com"
          } :
          # TODO make WS_ENDPOINT, API_ENDPOINT and PROJECITYF_DOMAIN arguments
          # to this derivation
            pkgs.buildNpmPackage {
              name = "projectify-frontend";
              src = ./.;
              npmDepsHash = "sha256-kQYmbdbSlUyKd0b3tvctcNYY41mbpf35YoLGQSRGgfQ=";
              nativeBuildInputs = [
                # For git rev-parse
                pkgs.git
              ];
              preConfigure = ''
                export VITE_WS_ENDPOINT=${wsEndpoint}
                export VITE_API_ENDPOINT=${apiEndpoint}
                export VITE_PROJECTIFY_DOMAIN=${projectifyDomain}
                export VITE_GIT_COMMIT_DATE=${self.lastModifiedDate}
                export VITE_GIT_BRANCH_NAME=nix
                export VITE_GIT_COMMIT_HASH=${self.rev or "dirty"}
                export NODE_ENV=production
              '';
              installPhase = ''
                mkdir -p $out
                cp -a build/. $out/
              '';
              meta = with pkgs.lib; {
                description = "Frontend for the Projectify project management software";
                homepage = "https://www.projectifyapp.com";
                license = with licenses; [ agpl3Only mit ];
                maintainers = [
                  {
                    name = "Justus Perlwitz";
                    email = "justus@jwpconsulting.net";
                  }
                ];
              };
            };
      in
      {
        inherit self nixpkgs;
        lib = {
          inherit mkFrontend;
        };
        packages = {
          projectify-frontend = mkFrontend {};
        };
        devShell = pkgs.mkShell {
          buildInputs = [
            nodejs
          ];
        };
      });
}
