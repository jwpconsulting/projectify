{
  description = "Flake utils demo";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/24.05";

    projectify-frontend.url = "path:../frontend";
    projectify-backend.url = "path:../backend";

    projectify-frontend.inputs.nixpkgs.follows = "nixpkgs";
    projectify-backend.inputs.nixpkgs.follows = "nixpkgs";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, projectify-frontend, projectify-backend }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        frontend = projectify-frontend.lib.${system}.mkFrontend {
            wsEndpoint = "/ws";
            apiEndpoint = "/api";
            projectifyDomain = "http://localhost:5000";
            adapter = "node";
        };
        backend = projectify-backend.packages.${system}.projectify-backend;
        static = projectify-backend.packages.${system}.projectify-backend-static;
        nodejs = pkgs.nodejs_20;
      in
      {
        packages = {
          default = pkgs.hello;
        };
        devShell = pkgs.mkShell {
          buildInputs = [
            backend
            frontend
            pkgs.python311Packages.supervisor
            pkgs.unixtools.watch
            pkgs.coreutils
            pkgs.caddy
            nodejs
          ];
          shellHook = ''
            export STATIC_ROOT=${static}
            export PROJECTIFY_FRONTEND_PATH=${frontend}
            export DJANGO_SETTINGS_MODULE=projectify.settings.development_nix
            export DJANGO_CONFIGURATION=DevelopmentNix
          '';
        };
      });
}
