# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
{ buildNpmPackage
, importNpmLock
, nodejs
}:

buildNpmPackage {
  name = "tailwind-deps";
  src = ./.;
  npmDeps = importNpmLock {
    npmRoot = ./projectify/theme/static_src;
  };
  buildInputs = [ nodejs ];
  preConfigure = ''
    cd projectify/theme/static_src
  '';
  installPhase = ''
    mkdir $out
    cp -r ../static/css/dist $out/dist
  '';
  npmConfigHook = importNpmLock.npmConfigHook;
}
