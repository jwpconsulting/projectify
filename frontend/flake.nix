# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
# Nix Flakes file
{
  description = "Projectify frontend";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";

    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        projectify-frontend-static = pkgs.callPackage ./build-frontend.nix {
          adapter = "static";
          inherit (self) lastModifiedDate;
          rev = self.rev or "dirty";
        };
        projectify-frontend-node =
          let
            frontend = (pkgs.callPackage ./build-frontend.nix {
              adapter = "node";
              inherit (self) lastModifiedDate;
              rev = self.rev or "dirty";
            });
          in
          pkgs.writeShellApplication {
            name = "projectify-frontend-node";
            runtimeInputs = [
              frontend
              frontend.passthru.nodejs
            ];
            text = ''
              exec node ${frontend}
            '';
          };
      in
      {
        inherit self nixpkgs;
        packages = {
          inherit projectify-frontend-static;
          inherit projectify-frontend-node;
        };
        devShell = pkgs.mkShell {
          buildInputs = [
            projectify-frontend-node.passthru.nodejs
          ];
        };
      });
}
