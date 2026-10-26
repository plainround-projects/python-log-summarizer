# make up | run | test | lint | down   (make help lists all)
UV ?= uv
RUN := $(UV) run --frozen
DATA := data
SAMPLE := $(DATA)/sample.log
SMALL := $(DATA)/small.log

-include .env
export

.PHONY: help up run run-small demo-memory test test-unit lint format audit check build install-check mutation-check clean down

help: ## list the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed -E 's/:.*## /\t/' | sort

# There is no service to start: "up" installs the locked environment and writes the lesson's sample logs.
up: ## install the locked environment and generate data/sample.log (500,000 lines) and data/small.log (20 lines)
	$(UV) sync --frozen
	mkdir -p $(DATA)
	$(RUN) logsum-make-log $(SAMPLE)
	$(RUN) logsum-make-log $(SMALL) --small

run: ## summarize the 500,000-line sample log, with elapsed time and peak memory
	$(RUN) logsum $(SAMPLE) --stats

run-small: ## summarize the 20-line log; the p95 must be 19.95
	$(RUN) logsum $(SMALL) --stats

demo-memory: ## the failure mode: peak memory of streaming vs readlines() on a tenth of the log and on all of it
	$(RUN) python scripts/compare_memory.py $(SAMPLE)

test: ## all tests (unit, integration, end to end) with coverage; domain and application must stay at 95% or more
	$(RUN) pytest --cov=logsum --cov-report=term
	$(RUN) coverage report --include='src/logsum/domain/*,src/logsum/application/*' --fail-under=95

test-unit: ## unit tests only
	$(RUN) pytest tests/unit

lint: ## ruff check, ruff format check, mypy --strict, import-linter
	$(RUN) ruff check .
	$(RUN) ruff format --check .
	$(RUN) mypy
	$(RUN) lint-imports

format: ## apply ruff's formatting and safe fixes
	$(RUN) ruff check --fix .
	$(RUN) ruff format .

audit: ## check the locked dependencies for known vulnerabilities
	$(UV) export --frozen --no-emit-project --format requirements-txt --output-file .audit-requirements.txt
	$(RUN) pip-audit --no-deps --disable-pip -r .audit-requirements.txt
	rm -f .audit-requirements.txt

check: lint test ## lint and test

build: ## build the wheel and source archive into dist/
	$(UV) build

install-check: ## step 6: install the wheel into a fresh virtual environment and run logsum there
	./scripts/install_check.sh $(SAMPLE)

mutation-check: ## step 5: change the latency suffix from ms to s in a scratch copy; the tests must fail
	./scripts/mutation_check.sh

down: ## remove the generated logs and local build output
	rm -rf $(DATA) dist .pytest_cache .mypy_cache .ruff_cache .import_linter_cache .coverage .audit-requirements.txt

clean: down
	rm -rf .venv
