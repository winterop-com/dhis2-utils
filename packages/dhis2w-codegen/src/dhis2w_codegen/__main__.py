"""Allow `python -m dhis2w_codegen ...` as an equivalent to the installed script."""

from dhis2w_codegen.cli import app

if __name__ == "__main__":
    app()
