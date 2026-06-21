# OkCupid

Portfolio data science project analyzing OkCupid profile data to explore patterns in demographics, lifestyle preferences, and relationship-related outcomes.

## Project summary

This project uses the OkCupid dataset to perform data cleaning, exploratory analysis, and predictive modeling. The workflow is centered in a Jupyter notebook and supported by reusable Python modules in the local package.

Primary notebook:
- `ntb/OkCupid.ipynb`

## Dataset

Project data is organized under `data/`:
- `data/raw/` - original source files
- `data/plt/` - plotting-ready tables or exports
- `data/mle/` - machine-learning-ready datasets and artifacts

The analysis typically includes profile-level features such as age, sex, orientation, education, religion, body type, location, and text-based fields.

## Project structure

```text
OkCupid/
|- assets/
|- cfg/
|- data/
|  |- raw/
|  |- plt/
|  |- mle/
|- ntb/
|  |- OkCupid.ipynb
|  |- solutions/
|- src/
|  |- okc/
|- styles/
|- Starter Files/
|- Sample Solution/
|- My Solution/
|- pyproject.toml
|- poetry.lock
|- LICENSE
`- README.md
```

## Tech stack

- Python 3.11-3.12
- pandas, numpy, scipy
- matplotlib, seaborn
- scikit-learn
- jinja2
- pyyaml
- Jupyter Notebook
- Poetry for dependency management

## Setup

1. Open a terminal in this project folder.
2. Install dependencies:

```bash
poetry install
```

3. Launch Jupyter:

```bash
poetry run jupyter notebook
```

4. Open `ntb/OkCupid.ipynb`.

## Analysis workflow

Typical workflow in this project:
1. Load raw profile data from `data/raw/`.
2. Clean missing values and normalize categorical fields.
3. Engineer features for visualization and modeling.
4. Explore distributions and relationships across profile attributes.
5. Train and evaluate machine learning models for selected prediction tasks.
6. Export intermediate and final outputs to `data/plt/` and `data/mle/`.

## Reproducibility notes

- Dependencies are pinned in `pyproject.toml` and `poetry.lock`.
- Reusable code is organized in `src/okc/`.
- Solution and starter material are included for comparison and learning.

## License

MIT License. See `LICENSE` for details.
