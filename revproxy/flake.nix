{
  description = "Reverse proxy configuration";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/24.05";

    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        caddyfile = pkgs.runCommand "Caddyfile" {} ''
          mkdir $out
          echo "
            :5000 {
              handle /admin/* {
                reverse_proxy :5002
              }
              handle /backend/static/* {
                reverse_proxy :5002
              }
              handle /ws/* {
                reverse_proxy :5002
              }
              handle_path /api/* {
                reverse_proxy :5002
              }
              handle /* {
                reverse_proxy :5001
              }
            }
          " | ${pkgs.caddy}/bin/caddy fmt - > $out/Caddyfile
        '';
        projectify-revproxy = pkgs.writeShellApplication {
          name = "projectify-revproxy";
          runtimeInputs = [ pkgs.caddy ];
          text = ''
            exec caddy --config "${caddyfile}/Caddyfile" run
          '';
        };
      in
      {
        packages = {
          default = projectify-revproxy;
          inherit projectify-revproxy;
        };
        devShell = pkgs.mkShell {
          buildInputs = [
            projectify-revproxy
          ];
        };
      });
}
