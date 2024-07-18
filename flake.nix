{
  description = "Projectify app Nix flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/24.05";

    projectify-frontend.url = "path:./frontend";
    projectify-backend.url = "path:./backend";
    projectify-revproxy.url = "path:./revproxy";

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
        packages = {
          projectify-frontend-node-container = pkgs.dockerTools.buildLayeredImage {
            name = "projectify-frontend-node";
            tag = "latest";
            contents = [
              frontend
            ];
            config = {
              Command = [ "projectify-frontend-node" ];
            };
          };
          projectify-backend-container = pkgs.dockerTools.buildLayeredImage {
            name = "projectify-backend";
            tag = "latest";
            contents = [
              backend
              manage
            ];
            config = {
              Command = [ "projectify-backend" ];
            };
          };
          projectify-celery-container = pkgs.dockerTools.buildLayeredImage {
            name = "projectify-celery";
            tag = "latest";
            contents = [
              backend
              manage
            ];
            config = {
              Command = [ "projectify-celery" ];
            };
          };
          projectify-revproxy-container = pkgs.dockerTools.buildLayeredImage {
            name = "projectify-revproxy";
            tag = "latest";
            contents = [
              revproxy
            ];
            config = {
              Command = [ "projectify-revproxy" ];
            };
          };
          skopeo = pkgs.skopeo;
        };
        devShell = pkgs.mkShell {
          buildInputs = [
            backend
            frontend
            revproxy
            celery
            manage
            pkgs.skopeo
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
