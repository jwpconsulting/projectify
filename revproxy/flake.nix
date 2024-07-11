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
        # https://ryantm.github.io/nixpkgs/builders/trivial-builders/#chap-trivial-builders
        caddyfileFormatted = pkgs.runCommand "Caddyfile" {} ''
          mkdir $out
          ${pkgs.caddy}/bin/caddy fmt - <${./Caddyfile} > $out/Caddyfile
        '';
        projectify-revproxy = pkgs.writeShellApplication {
          name = "projectify-revproxy";
          runtimeInputs = [ pkgs.caddy ];
          text = ''
            exec caddy --config "${caddyfileFormatted}/Caddyfile" run
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
