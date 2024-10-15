# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
# Nix Flakes file
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
        mkFrontend =
          { wsEndpoint ? "/ws"
          , apiEndpoint ? "/api"
          , projectifyDomain ? "https://www.projectify.com"
          , adapter ? "node"
          }:
          # TODO make WS_ENDPOINT, API_ENDPOINT and PROJECITYF_DOMAIN arguments
          # to this derivation
          pkgs.buildNpmPackage {
            name = "projectify-frontend";
            src = ./.;
            npmDepsHash = "sha256-Ci4Sw6X+NM+xTL4xgBufLPP1qtBZQ8tfXh9XxFxItYk=";
            buildInputs = [
              nodejs
            ];

            preConfigure = ''
              export VITE_WS_ENDPOINT=${wsEndpoint}
              export VITE_API_ENDPOINT=${apiEndpoint}
              export VITE_PROJECTIFY_DOMAIN=${projectifyDomain}
              export VITE_GIT_COMMIT_DATE=${self.lastModifiedDate}
              export VITE_GIT_BRANCH_NAME=nix
              export VITE_GIT_COMMIT_HASH=${self.rev or "dirty"}
              export PROJECTIFY_FRONTEND_ADAPTER=${adapter}
              export NODE_ENV=production
            '';

            postBuild =
              if adapter == "node" then ''
                cp -a package.json node_modules build/
              '' else "";

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
        projectify-frontend-static = mkFrontend { adapter = "static"; };
        projectify-frontend-node =
          let
            frontend = (mkFrontend { adapter = "node"; });
          in
          pkgs.writeShellApplication {
            name = "projectify-frontend-node";
            runtimeInputs = [
              frontend
              nodejs
            ];
            text = ''
              exec node ${frontend}
            '';
          };
      in
      {
        inherit self nixpkgs;
        lib = {
          inherit mkFrontend;
        };
        packages = {
          inherit projectify-frontend-static;
          inherit projectify-frontend-node;
        };
        devShell = pkgs.mkShell {
          buildInputs = [
            nodejs
          ];
        };
      });
}
