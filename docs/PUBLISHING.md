# Docs Publishing

This project publishes Sphinx docs to GitHub Pages via `.github/workflows/docs-pages.yml`.

## One-Time Repository Setup
1. Go to **Settings -> Pages** in the GitHub repository.
2. Set **Build and deployment** source to **GitHub Actions**.

## How Publishing Works
- Workflow: `Docs Pages`
- Triggered on pushes to `main` when docs/source files change, or manual dispatch.
- Builds docs with:
  - `sphinx-build -W -b html docs docs/_build/html`
- Deploys to GitHub Pages using `actions/deploy-pages`.

## Published URL
- `https://jlsteenwyk.github.io/gh-skyline-python/`
