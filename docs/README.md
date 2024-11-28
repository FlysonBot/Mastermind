# Instructions for Building the Documentation

## 1. Update the RST Files

CD to the directory of this project, then run:

```bash
sphinx-apidoc -o docs/source src/mastermind -f --templatedir=docs/source/_templates --maxdepth=2 --module-first
```

## 2. Build the Documentation

CD to the docs directory and run:

```bash
make clean
make html
```

The first command will delete the already built documentation. The second command will build the documentation.

If you encounter warning that says "more than one target found for cross-reference 'xxx'", you can ignore it.

## Troubleshooting

If you cannot run the `sphinx-apidoc` command, make sure you have the `sphinx` package installed by running:

```bash
pip install sphinx
```

If you are missing theme, install the theme by:

```bash
pip install sphinx-rtd-theme
```

If you cannot run the make command (especially on Windows), ensure you have `make` installed.
