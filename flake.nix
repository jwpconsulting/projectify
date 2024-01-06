{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.simpleFlake {
      inherit self nixpkgs;
      name = "Projectify frontend";
      shell = ./shell.nix;
    };
}
