{
  description = "Flake utils demo";

  inputs = {
    projectify-frontend.url = "../frontend";
    projectify-frontend.inputs.nixpkgs.follows = "projectify-backend/nixpkgs";
    projectify-backend.url = "../backend";

    nixpkgs.follows = "projectify-backend/nixpkgs";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, projectify-frontend, projectify-backend }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        backend = projectify-backend.packages.${system};
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            backend.projectify-backend
            pkgs.python311Packages.supervisor
            pkgs.unixtools.watch
            pkgs.coreutils
            pkgs.caddy
          ];
        };
      });
}
