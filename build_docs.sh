rm -rf ./docs/build
sphinx-apidoc -feo docs/source/ ./src/pqca
sphinx-build -aEb html docs/source/ docs/build/