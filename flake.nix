# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
{
  description = "Projectify app Nix flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";

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
        caddyFileTestEnv = pkgs.writeText "caddy-envfile" ''
          HOST=http://localhost
          PORT=80
          BACKEND_HOST=localhost
          BACKEND_PORT=1000
        '';
        caddyfileFormatted = pkgs.runCommand "Caddyfile" { } ''
          mkdir $out
          ${pkgs.caddy}/bin/caddy fmt - <${./Caddyfile} > $out/Caddyfile
          ${pkgs.caddy}/bin/caddy validate \
            --envfile ${caddyFileTestEnv} \
            --config $out/Caddyfile
        '';
        projectify-revproxy = pkgs.writeShellApplication {
          name = "projectify-revproxy";
          runtimeInputs = [ pkgs.caddy ];
          text = ''
            exec caddy --config ${caddyfileFormatted}/Caddyfile run
          '';
        };

        tailwind-deps = pkgs.callPackage ./build-tailwind-deps.nix { };
        projectify-bundle = pkgs.callPackage ./build-projectify-bundle.nix {
          inherit tailwind-deps;
          poetry2nix = poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
        };
      in
      {
        packages = rec {
          inherit projectify-bundle;
          projectify-manage = pkgs.writeShellApplication {
            name = "projectify-manage";
            runtimeInputs = [ projectify-bundle.dependencyEnv ];
            # TODO consider whether STATIC_ROOT is reallse needed to run a
            # management comma
            text = ''
              export STATIC_ROOT="${projectify-bundle.static}"
              exec ${projectify-bundle}/bin/manage.py "$@"
            '';
          };
          projectify-backend = pkgs.writeShellApplication {
            name = "projectify-backend";
            runtimeInputs = [ projectify-bundle.dependencyEnv ];
            text = ''
              export STATIC_ROOT="${projectify-bundle.static}"
              exec gunicorn --config ${projectify-bundle}/etc/gunicorn.conf.py --log-config ${projectify-bundle}/etc/gunicorn-error.log --access-logfile -
            '';
          };
          projectify-celery = pkgs.writeShellApplication {
            name = "projectify-celery";
            runtimeInputs = [ projectify-bundle.dependencyEnv ];
            # TODO make worker independent of STATIC_ROOT
            text = ''
              export STATIC_ROOT="${projectify-bundle.static}"
              exec celery --app projectify.celery worker --concurrency 1
            '';
          };

          projectify-backend-container = pkgs.dockerTools.streamLayeredImage {
            name = "projectify-backend";
            tag = "latest";
            contents = [
              projectify-backend
              projectify-manage
            ];
            config = {
              Cmd = [ "projectify-backend" ];
            };
          };
          projectify-celery-container = pkgs.dockerTools.streamLayeredImage {
            name = "projectify-celery";
            tag = "latest";
            contents = [
              projectify-celery
            ];
            config = {
              Cmd = [ "projectify-celery" ];
            };
          };
          # Run with
          # HOST=http://localhost \
          #     PORT=8001 \
          #     BACKEND_HOST=http://localhost \
          #     BACKEND_PORT=8000 \
          #     result/bin/projectify-revproxy
          inherit projectify-revproxy;
          projectify-revproxy-container = pkgs.dockerTools.streamLayeredImage {
            name = "projectify-revproxy";
            tag = "latest";
            contents = [
              projectify-revproxy
            ];
            config = {
              Cmd = [ "projectify-revproxy" ];
            };
          };

          skopeo = pkgs.skopeo;
        };
        devShell = pkgs.mkShell {
          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ projectify-bundle.passthru.postgresql ];
          buildInputs = [

            # TODO I temporarily commented out these build inputs. Are they
            # still needed?
            # backend
            # revproxy
            # celery
            # manage

            # Run things locally
            pkgs.redis
            pkgs.python312Packages.supervisor
            pkgs.librsvg

            # Test docker stuff
            pkgs.skopeo
            pkgs.podman-compose
            pkgs.hadolint

            # Docs
            pkgs.nodePackages.prettier

            # For backend development
            projectify-bundle.passthru.postgresql
            projectify-bundle.passthru.postgresql.pg_config
            pkgs.openssl
            pkgs.gettext
            pkgs.stripe-cli

            # License
            pkgs.reuse
          ];
        };
      });
}
