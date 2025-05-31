# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
{ lib

, nodejs_20
, buildNpmPackage
, importNpmLock

, wsEndpoint ? "/ws"
, apiEndpoint ? "/api"
, projectifyDomain ? "https://www.projectify.com"
, adapter ? "node"

, lastModifiedDate
, rev
}:
# TODO make WS_ENDPOINT, API_ENDPOINT and PROJECITYF_DOMAIN arguments
# to this derivation
buildNpmPackage {
  name = "projectify-frontend";
  srcs = [
    ./.
    ../LICENSES
  ];
  sourceRoot = "frontend";
  npmDeps = importNpmLock { npmRoot = ./.; };
  npmConfigHook = importNpmLock.npmConfigHook;
  buildInputs = [
    nodejs_20
  ];
  prePatch = ''
    # Patch LICENSES folder into here, removing the symlink first
    rm LICENSES
    cp -r ../LICENSES .
  '';

  preConfigure = ''
    export VITE_WS_ENDPOINT=${wsEndpoint}
    export VITE_API_ENDPOINT=${apiEndpoint}
    export VITE_PROJECTIFY_DOMAIN=${projectifyDomain}
    export VITE_GIT_COMMIT_DATE=${lastModifiedDate}
    export VITE_GIT_BRANCH_NAME=nix
    export VITE_GIT_COMMIT_HASH=${rev}
    export PROJECTIFY_FRONTEND_ADAPTER=${adapter}
    export NODE_ENV=production
  '';

  postBuild =
    if adapter == "node" then ''
      cp -a package.json node_modules build/
    '' else "";

  installPhase = ''
    mkdir -p $out
    cp -a build/. $out/
  '';

  passthru = {
    nodejs = nodejs_20;
  };
  meta = with lib; {
    description = "Frontend for the Projectify project management software";
    homepage = "https://www.projectifyapp.com";
    license = with licenses; [ agpl3Only mit ];
    maintainers = [
      {
        name = "Justus Perlwitz";
        email = "justus@jwpconsulting.net";
      }
    ];
  };
}
