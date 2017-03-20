with import <nixpkgs> {}; {
  migrateEnv = stdenv.mkDerivation {
    name = "migrate-env";
    buildInputs = [ stdenv python27Full python27Packages.virtualenv ];
    shellHook = ''
      if [ ! -d venv ]; then
        virtualenv --python=python2.7 venv
        ./venv/bin/pip install -r requirements.txt
      fi
    '';
  };
}
