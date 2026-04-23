# CSCI 164 — Final Project: Applied ML with scikit-learn

**Authors:** Tanay Malavia, Darpan Attri, Andres Ramos, Harika Yendapalli
**Course:** CSCI 164 — Artificial Intelligence (Spring 2026)
**Due:** April 26, 2026

## Overview
Supervised learning study on two datasets using three algorithms each, with hyperparameter tuning and comparison to prior published work.

## Datasets
1. **Titanic — Survival Prediction** (classification, binary) — Kaggle
2. **California Housing — Median House Value** (regression) — sklearn built-in

## Models
| Dataset       | Algorithms                                        |
|---------------|---------------------------------------------------|
| Titanic       | Logistic Regression, k-NN, Decision Tree          |
| CA Housing    | Linear Regression, Decision Tree Regressor, MLP   |

## Structure
```
final-project/
├── notebooks/       # Jupyter notebooks, one per phase
├── data/            # Raw + processed data (gitignored if large)
├── figures/         # Saved plots for the report
├── report/          # Executive summary PDF
└── requirements.txt
```

## Reproducibility

### 1. Set up the environment
```bash
cd final-project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> If you rename or move the project folder, delete `.venv/` and recreate it — virtual environments store absolute paths.

### 2. Get the data
- **Titanic** — download `train.csv` from https://www.kaggle.com/c/titanic/data, rename it `titanic.csv`, and place it in `data/`.
- **California Housing** — no action needed; `sklearn.datasets.fetch_california_housing` downloads it automatically on first run.

### 3. Run the notebooks
```bash
jupyter lab
```
Then open and run all cells, in order:
1. `notebooks/01_titanic.ipynb`
2. `notebooks/02_california_housing.ipynb`

Figures are saved to `figures/`. Runtime is ~1–2 minutes per notebook.

## Workflow
1. EDA + preprocessing
2. Baseline models
3. Hyperparameter tuning (GridSearchCV)
4. Evaluation + literature comparison
5. Summary report + presentation
