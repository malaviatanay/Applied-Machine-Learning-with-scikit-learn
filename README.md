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
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Workflow
1. EDA + preprocessing
2. Baseline models
3. Hyperparameter tuning (GridSearchCV)
4. Evaluation + literature comparison
5. Summary report + presentation
