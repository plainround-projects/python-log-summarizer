# Changelog

All notable changes to this project are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-10-26

### Added

- `logsum`, a command-line tool that streams an access log and prints requests per status, the ten slowest paths by 95th-percentile latency and the number of unparseable lines; `--json`, `--top`, `--stats` (elapsed time and peak memory), `--estimator exact|histogram`.
- Transparent reading of `.gz` logs; a fixed-size histogram estimator with a stated accuracy bound.
- `logsum-make-log`, the lesson's sample-log generator with a seed, and the 20-line log whose p95 is 19.95.
- Layered package (`domain`, `application`, `infrastructure`, `interfaces`) with the dependency rule enforced by import-linter.
- Unit, integration and end-to-end tests with coverage (domain and application at 100%), `mypy --strict`, ruff, `uv.lock`, a CI workflow, `make mutation-check` and `make install-check`.
- JSON Schema for the `--json` output; four decision records.
