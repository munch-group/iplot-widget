# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`iplot` is a small Python library (single module) that wraps seaborn plotting
functions in Jupyter/`ipywidgets` dropdowns, so a user can call `iplot(dataframe)`
and interactively pick `x`, `y`, `hue`, `row`, `col`, and plot type without writing
new plotting code per chart. All the logic lives in `src/iplot/iplot.py`, exposing
`iplot()` and `iplot_settings()` (re-exported from `src/iplot/__init__.py`).

The repo was generated from the `munch-group` library template
(`munch-group/munch-group-library`) and is kept in sync with it; `scripts/rename.py`
is the template's own one-shot rename script (a no-op here since this repo was
already renamed away from the template's placeholder name).

## Environment & commands

Environment/dependencies are managed with **pixi** (`pixi.lock`, `pyproject.toml`
`[tool.pixi.*]` tables), not plain pip/conda. Run everything through `pixi run
<task>` (or `pixi shell` to drop into the env).

```bash
pixi install --locked   # set up the environment (also devcontainer postCreateCommand)
pixi run install-dev    # editable install of iplot into the pixi env
pixi run test           # convert docs/pages/tutorial/*.ipynb to pytest modules and run them
pixi run docs           # execute docs notebooks in place
pixi run api            # build+render the quartodoc/Quarto site (docs/api/, docs/_build/)
pixi run commit         # stage-aware commit with an AI-drafted message (needs ANTHROPIC_API_KEY), then push
pixi run bump           # bump pyproject.toml version and commit (args: kind=patch/minor/major, flag=--pre/--release)
pixi run release        # bump + push + tag + GitHub release -> triggers conda/PyPI publish
pixi run version        # release, gated on test+api+docs+commit succeeding first
pixi run clean          # git clean -id (interactive)
```

Tests live as a notebook, not a package: `docs/pages/tutorial/test_iplot.ipynb`
holds `def test_*():` functions exercising iplot's public API (`iplot()`,
`iplot_settings()`, `AX2FIG`). `pixi run test` converts it to a script via
`jupyter nbconvert --to script` into `tests/pytest/tmp/` (gitignored, regenerated
every run) and runs it with pytest. To add a test, add a `test_*` function to
that notebook — a plain `.py` file dropped in `tests/` won't be picked up.

**Known gotcha:** `iplot/__init__.py` does `from .iplot import iplot`, which
rebinds the `iplot` package's `.iplot` attribute from the submodule to the
function. `import iplot.iplot as x` therefore silently binds `x` to the
*function*, not the submodule — use `importlib.import_module("iplot.iplot")`
to reach the submodule (e.g. for its `OPTIONS`/`AX2FIG` globals), as the test
notebook does.

The package version is set in **two places that must stay in sync**:
`pyproject.toml` `[project].version` and `[tool.pixi.workspace].version`. The
`bump` task updates both via `scripts/bump_version.py`.

**License mismatch:** `pyproject.toml` declares MIT, but `LICENSE` is the full
GPLv3 text. This predates this sync (inherited from the template) — flag it
rather than assuming either is correct if it comes up.

## Packaging & docs publishing (CI-driven)

- Conda package metadata lives in `conda-build/meta.yaml` / `conda-build/build_env.yaml`,
  which read dependencies and entry points from `pyproject.toml`. Pushing a
  `vX.Y.Z` / `vX.Y.Z.rcN` tag triggers `.github/workflows/conda-release.yml` to
  build conda packages (macOS + Linux by default — the matrix has a commented-out
  block to restore the wider linux/osx/win × multi-python matrix) and publish to
  the `munch-group` anaconda channel (needs the `ANACONDA_TOKEN` secret), plus
  create a GitHub release with an auto-generated changelog.
- The same tag also triggers `.github/workflows/pypi-release.yml`, which builds
  an sdist + universal wheel and publishes to PyPI via `pypa/gh-action-pypi-publish`.
  **This needs a `PYPI_API_TOKEN` repo secret that does not exist yet** — until
  it's added, this workflow will fail on every tag push (harmlessly; it doesn't
  block the conda workflow).
- Docs are a Quarto + quartodoc website under `docs/` (`docs/_quarto.yml`),
  published to GitHub Pages on every push to `main` via
  `.github/workflows/quarto-publish.yml`. `quartodoc` autogenerates API reference
  pages (`docs/api/`) from docstrings in `src/iplot/`; source files for the
  manual/example pages are `docs/pages/*.qmd` and `docs/examples/*.ipynb`. Use
  numpy-style docstrings (see `docs/autodoc.mustache` for the VS Code
  autoDocstring template referenced in `README.md`). Note the CI workflow
  installs iplot itself (`pip install jupyter -e .`) before rendering, because
  `docs/pages/getting_started.qmd` actually calls `import iplot` — don't drop
  that `-e .` when touching the workflow, it's not template boilerplate.
- `pixi run docs` (execute notebooks in place) and `pixi run api` (build+render)
  are separate tasks now — run both to fully rebuild docs locally.
  `docs/_build`, `docs/_freeze`, and `docs/.quarto` are generated output, not source.

## Code review kit

`.claude/agents/code-{python,api-consistency,ui-heuristics}-reviewer.md` +
`.claude/commands/review*.md` (`review-kit/` has the docs) provide `/review
<file>` (parallel specialist review → one report under `.claude/review-reports/`)
and `/review-apply` (apply findings in small test-gated batches). Run
`/review-init` once before first use — it fills in the `{{TARGET_FILE}}` /
`{{TEST_COMMAND}}` / `{{LINT_COMMAND}}` placeholders still in those files. The
frontend and theming specialists were dropped during this sync — iplot has no
CSS/JS/HTML/theming system for them to review.

## Architecture notes for `src/iplot/iplot.py`

- `OPTIONS` (module-level dict) holds global defaults — default figure size,
  facet sizing bounds, the seaborn theme dict, and the list of allowed
  "axis-level" seaborn graphics functions. `iplot_settings(**kwargs)` mutates
  this dict; it's the only supported way to change defaults (e.g. restrict
  which plot kinds show up, or set default axis variables).
- `AX2FIG` maps a short plot "kind" (e.g. `'scatter'`, `'box'`) to the seaborn
  *figure-level* function that implements it (`relplot`/`displot`/`catplot`/`lmplot`).
  `iplot()` always renders through a figure-level call (never calls the
  axis-level functions in `AXIS_LEVEL_GRAPHICS` directly) — that list is only
  used to populate the "Plot" dropdown and to introspect each function's
  signature (via `inspect.signature`) to decide which plot kinds are valid
  given the currently selected `x`/`y`/`hue`/`row`/`col`.
- The dropdowns are wired reactively: every dimension dropdown's `observe`
  callback (`_set_graphics_options`) recomputes the valid `plot` options
  whenever `x`/`y`/`hue`/`row`/`col` changes, by intersecting each candidate
  function's parameter names with the currently-set dimensions.
- Facet sizing for `row`/`col` facets is computed by hand from `OPTIONS`
  (`max_figure_width/height`, `min/max_facet_height`) rather than left to
  seaborn defaults — see the `find_facet_size` binary search in `_plot` for the
  col-only case. Be careful modifying this: it's tuned to keep faceted figures
  within a bounded overall canvas size regardless of the number of category
  levels.
- Clicking "Show plot" (`_plot` callback) also renders a collapsible
  "Show code for plot" Markdown block reproducing the equivalent
  `sns.<figure_level_fn>(...)` call, so users can copy runnable code — keep
  this in sync if you change how `_kwargs`/`extra_kwargs` are assembled.
- There is a large block of commented-out legacy implementation at the bottom
  of `__init__.py` (an older axis-level-only version of `iplot`) — dead code,
  not a reference for current behavior.
