# CLAUDE.md

## Project Overview
FREEd6 is a rules-light tabletop RPG system by Jeremy Deram. The repo contains the game rules (as markdown) and a browser-based character generator written in plain JavaScript, served by GitHub Pages at https://jderam.github.io/FREEd6 with no backend and no external dependencies.

## Rules Are the Source of Truth
- The markdown rules docs in `rules/` are the source of truth for the game. The character generator code (`html/js/chargen.js` and `html/js/data.js`) is derived from them, never the other way round.
- Whenever a rules doc is changed, audit the generator code against the changed rules and tell Jeremy whether any code updates are needed, listing each mismatch. Report first; don't silently change the code to match.
- Where the code and the rules disagree, the rules win. Known disagreements are listed in `TODO.md`.

## Repository Structure
- `rules/` — Game rules in markdown, organized into `book1/`, `book2/`, and `misc/`
- `html/` — Character generator site (`index.html`, `chargen.html`, `free_d6.css`)
  - `html/js/chargen.js` — character generation logic
  - `html/js/data.js` — game data tables
  - `html/js/zothique_names.js` — name lists for `name=auto`
  - `html/js/app.js` — reads the `level` and `name` query parameters and renders the page
  - `html/fonts/` — self-hosted web fonts
- `tests/js/` — JavaScript tests
- `changelog.md` — Project changelog (Keep a Changelog format)

## Common Commands
- `node tests/js/test_chargen.js` — Run the tests (plain Node, no packages to install)
- `python3 -m http.server 8000` — Serve the repo locally, then open `http://localhost:8000/html/chargen.html?level=1&name=auto`

## Code Style
- No build step, no npm packages, no CDN links: everything the page loads must live in this repo
- Scripts are classic `<script>` files that also export via `module.exports` so Node can load them in tests
- JavaScript uses 2-space indent and double quotes

## GitHub Pages
- Built by Jekyll from the `main` branch root, so the rules markdown is rendered with kramdown: a table needs a blank line above it, even directly under a heading

## CI
- GitHub Actions workflow (`.github/workflows/ci.yml`) runs the JavaScript tests on PRs

## Git Workflow
- Main branch: `main`
- PRs target `main`
