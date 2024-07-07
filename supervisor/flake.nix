{
  description = "Flake utils demo";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/24.05";

    projectify-frontend.url = "../frontend";
    projectify-backend.url = "../backend";

    projectify-frontend.inputs.nixpkgs.follows = "nixpkgs";
    projectify-backend.inputs.nixpkgs.follows = "nixpkgs";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, projectify-frontend, projectify-backend }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        frontend = projectify-frontend.packages.${system};
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
          shellHook = ''
            # TODO
            export PROJECTIFY_BACKEND_STATIC_PATH=${backend.projectify-backend}
            export PROJECTIFY_FRONTEND_PATH=${frontend.projectify-frontend}
          '';
        };
      });
}
