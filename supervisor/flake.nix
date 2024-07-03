{
  description = "Flake utils demo";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    projectify-frontend.url = "../frontend";
    projectify-frontend.inputs.nixpkgs.follows = "nixpkgs";
    projectify-backend.url = "../backend";
    projectify-backend.inputs.nixpkgs.follows = "nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, projectify-frontend, projectify-backend }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            pkgs.python311Packages.supervisor
            pkgs.unixtools.watch
            pkgs.coreutils
          ];
        };
      });
}
