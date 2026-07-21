
![](https://github.com/munch-group/iplot/actions/workflows/quarto-publish.yml/badge.svg?event=push)

# iplot

Interactive seaborn plotting widgets for Jupyter. Call `iplot(dataframe)` and
get dropdowns for `x`, `y`, `hue`, `row`, and `col` plus a plot-type picker —
explore a dataset's relationships without writing new plotting code for every
view.

See [munch-group.org/iplot](https://munch-group.org/iplot) for the full docs
and examples.

## Installation

```bash
conda install -c munch-group iplot
```

## Quick start

```python
import seaborn as sns
from iplot import iplot

data = sns.load_dataset('penguins')
iplot(data)
```

## Development

Environment and tasks are managed with [pixi](https://pixi.sh):

```bash
pixi install --locked   # set up the dev environment
pixi run install-dev    # editable install of iplot into it
pixi run test           # run the test suite
pixi run docs           # execute the docs notebooks in place
pixi run api            # build and render the quartodoc/Quarto site
```

Releasing a new version:

```bash
pixi run release        # bump the patch version, tag, and push
```

This triggers CI to build and publish the conda and PyPI packages and
publish the docs site.

## License

MIT — see [LICENSE](LICENSE).
