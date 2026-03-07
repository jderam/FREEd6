# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.2] - 2026-03-07
### Added
- CI checks for version increment and changelog entry on PRs
- Auto-tagging on merge to main after successful PyPI publish

### Fixed
- Corrected broken URL in browser-based character generator (`/free-d6/char` → `/free_d6/char`)

## [0.3.1] - 2026-03-07
### Added
- `scripts/gen_char_sheet.py`: command-line script to generate a printable single-page text character sheet

## [0.3.0] - 2026-02-14
### Added
- Unit tests for Character class and data module
- GitHub Actions CI workflow (lint + test across Python 3.11–3.14)
- GitHub Actions publish workflow (PyPI trusted publishers)

### Fixed
- Broken appendix links in README

### Changed
- Refactored Character class for clearer structure and fixed bugs
- Migrated build backend from setuptools to hatchling
- Modernized dev tooling (uv, ruff formatting, pre-commit hooks)
- Updated supported Python versions to 3.11–3.14
- Cleaned up Makefile (removed dead targets, prod deploy via GitHub Actions)

## [0.2.0] - 2024-10-28
### Changed
- Renamed repo `d666-rpg-system` -> `FREEd6`
- Renamed package `d666_rpg_system` -> `free_d6`
- Added 0-level functionality to `Character` class

## [0.1.1] - 2024-01-17
### Changed
- Renamed method `to_dict()` -> `as_dict()`

## [0.1.0] - 2024-01-17
### Changed
- Renamed repo from `d666-system` to `d666-rpg-system`
- Added character generation code to this repo
- Restructured rules markdown files into Book folders
- Added some new items

## [0.0.1] - 2023-09-29
### Created
- Initial version
