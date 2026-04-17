"""Allow `python -m dhis2_codegen ...` as an equivalent to the installed script."""

from dhis2_codegen.cli import app

if __name__ == "__main__":
    app()
