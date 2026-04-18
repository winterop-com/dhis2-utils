.PHONY: help install lint test test-slow test-durations coverage docs docs-serve docs-build migrate upgrade downgrade build publish-client deps-upgrade clean dhis2-run dhis2-down dhis2-seed dhis2-build-e2e-dump

UV := $(shell command -v uv 2> /dev/null)

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install          Sync workspace deps (all members, dev group included)"
	@echo "  lint             Run ruff format + ruff check + mypy + pyright"
	@echo "  test             Run tests (excludes slow)"
	@echo "  test-slow        Run slow tests only"
	@echo "  test-durations   Show 20 slowest tests"
	@echo "  coverage         Run tests with coverage reporting"
	@echo "  docs             Alias for docs-serve"
	@echo "  docs-serve       Serve mkdocs site locally at http://127.0.0.1:8000"
	@echo "  docs-build       Build mkdocs site to ./site"
	@echo "  migrate          Generate a new alembic migration (MSG='description')"
	@echo "  upgrade          Apply pending migrations"
	@echo "  downgrade        Revert last migration"
	@echo "  build            Build all workspace wheels"
	@echo "  publish-client   Upload dhis2-client wheel to PyPI (requires TWINE_* env)"
	@echo "  deps-upgrade     Re-resolve uv.lock to pick up newer versions"
	@echo ""
	@echo "  dhis2-run        Start the stack, seed auth, stream logs (Ctrl+C tears it down)"
	@echo "  dhis2-seed       (re-)seed PATs + OAuth2 client against an already-running stack"
	@echo "  dhis2-down       Stop the local DHIS2 stack"
	@echo "  dhis2-build-e2e-dump  Wipe + populate a fresh DHIS2 with test data, regenerate infra/dhis.sql.gz"
	@echo ""
	@echo "  For niche targets (versions, wait, status, logs, pat) use 'make -C infra help'."
	@echo ""
	@echo "  clean            Remove caches, build artifacts, coverage output"

install:
	@echo ">>> Syncing workspace"
	@$(UV) sync --all-packages --all-extras

lint:
	@echo ">>> Running linter"
	@$(UV) run ruff format .
	@$(UV) run ruff check . --fix
	@echo ">>> Running type checkers"
	@$(UV) run mypy --explicit-package-bases packages
	@$(UV) run pyright

test:
	@echo ">>> Running tests (excluding slow)"
	@$(UV) run pytest -q -m "not slow" packages

test-slow:
	@echo ">>> Running slow tests"
	@if [ -f infra/home/credentials/.env.auth ]; then \
		set -a; . infra/home/credentials/.env.auth; set +a; \
		$(UV) run pytest -v -m slow packages; \
	else \
		echo "    (no infra/home/credentials/.env.auth — integration tests that need it will skip; run 'make dhis2-run' first to populate it)"; \
		$(UV) run pytest -v -m slow packages; \
	fi

test-durations:
	@echo ">>> Running tests with 20 slowest"
	@$(UV) run pytest -q -m "not slow" --durations=20 packages

coverage:
	@echo ">>> Running tests with coverage"
	@$(UV) run coverage run -m pytest -q -m "not slow" packages
	@$(UV) run coverage report
	@$(UV) run coverage xml

docs-serve:
	@echo ">>> Serving docs at http://127.0.0.1:8000"
	@$(UV) run mkdocs serve

docs-build:
	@echo ">>> Building docs site"
	@$(UV) run mkdocs build

docs: docs-serve

migrate:
	@echo ">>> Generating migration: $(MSG)"
	@$(UV) run alembic revision --autogenerate -m "$(MSG)"
	@$(UV) run ruff format packages/dhis2-core/src/dhis2_core/alembic/versions

upgrade:
	@echo ">>> Applying pending migrations"
	@$(UV) run alembic upgrade head

downgrade:
	@echo ">>> Reverting last migration"
	@$(UV) run alembic downgrade -1

build:
	@echo ">>> Building all workspace wheels"
	@$(UV) build --all-packages

publish-client:
	@echo ">>> Building dhis2-client wheel"
	@$(UV) build --package dhis2-client
	@echo ">>> Publishing dhis2-client to PyPI (dry-run, set PUBLISH=1 to actually upload)"
	@if [ "$(PUBLISH)" = "1" ]; then \
		$(UV) publish dist/dhis2_client-*.whl dist/dhis2_client-*.tar.gz; \
	else \
		echo "    (skipped upload; run 'make publish-client PUBLISH=1' to push)"; \
	fi

deps-upgrade:
	@echo ">>> Upgrading all resolvable deps (uv lock --upgrade)"
	@$(UV) lock --upgrade
	@echo ">>> Re-syncing workspace with updated lock"
	@$(UV) sync --all-packages --all-extras

dhis2-run:
	@DHIS2_VERSION=$(or $(DHIS2_VERSION),42) infra/scripts/dhis2_run.sh

dhis2-seed:
	@$(MAKE) -C infra seed

dhis2-down:
	@$(MAKE) -C infra down

dhis2-build-e2e-dump:
	@$(MAKE) -C infra build-e2e-dump DHIS2_VERSION=$(or $(DHIS2_VERSION),42)

clean:
	@echo ">>> Cleaning"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .coverage htmlcov coverage.xml
	@rm -rf .pyright
	@rm -rf dist build site

.DEFAULT_GOAL := help
