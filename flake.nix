{
  description = "Projectify app Nix flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";

    flake-utils.url = "github:numtide/flake-utils";

    poetry2nix = {
      url = "github:nix-community/poetry2nix/master";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        frontend-flake = import ./frontend/flake.nix;
        frontend-outputs = frontend-flake.outputs {
          inherit self nixpkgs flake-utils;
        };
        frontend = frontend-outputs.packages.${system}.projectify-frontend-node;
        backend-flake = import ./backend/flake.nix;
        backend-outputs = backend-flake.outputs {
          inherit self nixpkgs flake-utils poetry2nix;
        };
        backend = backend-outputs.packages.${system}.projectify-backend;
        celery = backend-outputs.packages.${system}.projectify-celery;
        manage = backend-outputs.packages.${system}.projectify-manage;
        caddyfileFormatted = pkgs.runCommand "Caddyfile" {} ''
          mkdir $out
          ${pkgs.caddy}/bin/caddy fmt - <${./Caddyfile} > $out/Caddyfile
        '';
        revproxy = pkgs.writeShellApplication {
          name = "projectify-revproxy";
          runtimeInputs = [ pkgs.caddy ];
          text = ''
            exec caddy --config "${caddyfileFormatted}/Caddyfile" run
          '';
        };
        nodejs = pkgs.nodejs_20;
      in
      {
        packages = {
          projectify-frontend-node-container = pkgs.dockerTools.streamLayeredImage {
            name = "projectify-frontend-node";
            tag = "latest";
            contents = [
              frontend
            ];
            config = {
              Cmd = [ "projectify-frontend-node" ];
            };
          };
          projectify-backend-container = pkgs.dockerTools.streamLayeredImage {
            name = "projectify-backend";
            tag = "latest";
            contents = [
              backend
              manage
            ];
            config = {
              Cmd = [ "projectify-backend" ];
            };
          };
          projectify-celery-container = pkgs.dockerTools.streamLayeredImage {
            name = "projectify-celery";
            tag = "latest";
            contents = [
              celery
            ];
            config = {
              Cmd = [ "projectify-celery" ];
            };
          };
          projectify-revproxy-container = pkgs.dockerTools.streamLayeredImage {
            name = "projectify-revproxy";
            tag = "latest";
            contents = [
              revproxy
            ];
            config = {
              Cmd = [ "projectify-revproxy" ];
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
            pkgs.redis
            pkgs.hadolint
            pkgs.podman-compose
            pkgs.nodePackages.prettier
          ];
        };
      });
}
