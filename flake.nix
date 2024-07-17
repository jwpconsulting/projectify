{
  description = "Projectify app Nix flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/24.05";

    projectify-frontend.url = "path:frontend";
    projectify-backend.url = "path:backend";
    projectify-revproxy.url = "path:revproxy";

    projectify-frontend.inputs.nixpkgs.follows = "nixpkgs";
    projectify-backend.inputs.nixpkgs.follows = "nixpkgs";
    projectify-revproxy.inputs.nixpkgs.follows = "nixpkgs";


    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, projectify-revproxy, projectify-frontend, projectify-backend }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        frontend = projectify-frontend.packages.${system}.projectify-frontend-node;
        backend = projectify-backend.packages.${system}.projectify-backend;
        celery = projectify-backend.packages.${system}.projectify-celery;
        manage = projectify-backend.packages.${system}.projectify-manage;
        revproxy = projectify-revproxy.packages.${system}.projectify-revproxy;
        nodejs = pkgs.nodejs_20;
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            backend
            frontend
            revproxy
            celery
            manage
            pkgs.podman-compose
            pkgs.python311Packages.supervisor
            pkgs.keydb
            pkgs.hadolint
            pkgs.podman-compose
            pkgs.nodePackages.prettier
          ];
        };
      });
}
