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
    mkdir -p $out
    cp ../static/css/dist/styles.css $out/styles.css
  '';
  npmConfigHook = importNpmLock.npmConfigHook;
}
