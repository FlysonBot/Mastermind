# Instruction for Building the Documentation

## 1. Update the RST Files

CD to the directory of this project, the run:

``` Bash
sphinx-apidoc -o docs/source src/ -f --templatedir=docs/source/_templates --doc-project="Table of Content" --maxdepth=2 --module-first
```

## 2. Build the Documentation

CD to the docs directory and run:

``` Bash
make clean
make html
```

The first command will delete the already built documentation. The second command will build the documentation.

If you encounter warning that saids "more than one target found for cross-reference 'xxx'", you can ignore it.

## Troubleshooting

If you cannot run the `sphinx-apidoc` command, make sure you have the `sphinx` package installed by running:

``` Bash
pip install sphinx
```

If you are missing theme, install the theme by:

``` Bash
pip install sphinx-rtd-theme
```

If you cannot run the make command (especially on Windows), ensure you have `make` installed.
