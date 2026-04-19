# Executive Summary — CSCI 164 Final Project

**Author:** Tanay Malavia
**Course:** CSCI 164 — Artificial Intelligence, Spring 2026
**Date:** April 2026

---

## 1. Introduction (1/2 page)
- Problem: build and compare supervised ML models on two datasets.
- Datasets selected: Titanic (classification), California Housing (regression).
- Why these: small, well-documented, strong prior-work benchmarks, cover both classification and regression.

## 2. Datasets (1 page)

### 2.1 Titanic
- Source: Kaggle competition `titanic` — 891 rows, 11 features.
- Features: `Pclass`, `Sex`, `Age`, `SibSp`, `Parch`, `Fare`, `Embarked`, etc.
- Target: `Survived` (0/1).
- Preprocessing: drop ID/Name/Ticket/Cabin; median-impute `Age`; mode-impute `Embarked`; one-hot encode categoricals; standard-scale numerics.

### 2.2 California Housing
- Source: `sklearn.datasets.fetch_california_housing` (Pace & Barry 1997) — 20,640 rows, 8 features.
- Features: median income, house age, rooms, bedrooms, population, occupancy, lat/lon.
- Target: `MedHouseVal` ($100k units).
- Preprocessing: no missing values; StandardScaler for linear/MLP models.

## 3. Methods (1 page)

| Dataset | Model 1             | Model 2                | Model 3       |
|---------|---------------------|------------------------|---------------|
| Titanic | Logistic Regression | k-NN                   | Decision Tree |
| CA      | Linear Regression   | Decision Tree Regressor| MLP Regressor |

- **Validation:** 80/20 train/test split, 5-fold CV on training data.
- **Tuning:** `GridSearchCV` over key hyperparameters (C, k, max_depth, hidden_layer_sizes, alpha).
- **Metrics:** classification — accuracy, precision, recall, F1, ROC-AUC; regression — MAE, RMSE, R².

## 4. Results (1–2 pages)

### 4.1 Titanic
| Model  | Accuracy | Precision | Recall | F1     | ROC-AUC |
|--------|----------|-----------|--------|--------|---------|
| LogReg | 0.7933   | 0.7759    | 0.6522 | 0.7087 | 0.8472  |
| kNN    | 0.7989   | 0.7797    | 0.6667 | 0.7188 | 0.8489  |
| Tree   | 0.7877   | 0.8163    | 0.5797 | 0.6780 | 0.7827  |

**Winner: k-NN** — highest accuracy, F1, and ROC-AUC. Logistic Regression is a close second. The Decision Tree has the best precision (0.82) but the worst recall (0.58), meaning it underpredicts survival — a conservative decision boundary that misses too many survivors.

Figures: `figures/titanic_confusion.png`, `figures/titanic_roc.png`.

### 4.2 California Housing
| Model  | MAE    | RMSE   | R²     |
|--------|--------|--------|--------|
| Linear | 0.5332 | 0.7456 | 0.5758 |
| Tree   | 0.4041 | 0.5979 | 0.7272 |
| MLP    | 0.3448 | 0.5100 | 0.8015 |

**Winner: MLP** — lowest MAE and RMSE, highest R² by a clear margin. Linear Regression underfits (R² 0.58) because the income-to-value relationship is non-linear and the spatial signal cannot be captured linearly. The Decision Tree is intermediate.

Figures: `figures/ca_pred_vs_actual.png`, `figures/ca_residuals.png`.

## 5. Comparison to Prior Work

**Titanic.** Sehgal's widely-cited Kaggle notebook *Titanic Data Science Solutions* reports test accuracies of 0.77–0.84 across Logistic Regression, SVM, and Random Forest. Our tuned k-NN (0.7989) and Logistic Regression (0.7933) fall in the middle of that band. Sehgal's higher scores come from feature engineering we intentionally omitted — extracting `Title` from `Name`, binning `Age`, and engineering a `FamilySize` feature — plus ensemble methods not in our scope.

**California Housing.** Pace & Barry (1997) introduced this dataset and reported R² ≈ 0.65 using a sparse spatial autoregression. Modern sklearn benchmarks using `HistGradientBoostingRegressor` report R² ≈ 0.80–0.85. Our MLP (R² 0.8015) matches the modern benchmark band and substantially exceeds the 1997 baseline. The gap comes from the MLP's ability to capture the non-linear income-to-value relationship and to use latitude/longitude directly rather than through hand-crafted neighbor features.

## 6. Discussion

**Why k-NN edged out on Titanic.** The dataset is small (891 rows) and dominated by a few strong signals (`Sex`, `Pclass`, `Age`). k-NN with scaled features captures local structure without overfitting. The Decision Tree's high precision / low recall suggests it partitions aggressively on `Sex` and then over-prunes the "survived" branch — a typical behavior when `max_depth` is limited but class imbalance pulls predictions toward the majority.

**Why MLP won on California Housing.** `MedInc` is the strongest predictor but its relationship to `MedHouseVal` is non-linear (diminishing returns at the top end). Linear Regression cannot model this curvature — its R² of 0.58 is effectively a ceiling for purely linear methods. The Decision Tree can model non-linearity but splits are axis-aligned and greedy. The MLP's hidden layers approximate smooth non-linear interactions (e.g. income × location), which is why RMSE drops from 0.60 → 0.51.

**Limitations.**
- Titanic is small; the 80/20 split leaves only ~178 test samples, so metric differences of 1–2 points are within noise.
- California target is capped at $500k, which shows up as a flat band at the top of the predicted-vs-actual scatter and inflates residuals on high-value homes.
- We omitted ensemble methods per the rubric's focus on classical single models.

**Real-world relevance.** Both tasks mirror high-stakes applied settings — risk scoring for insurance and mortgage valuation for lending. The Titanic model's heavy dependence on `Sex` and `Pclass` is a reminder that models fit to historical outcomes inherit the biases of the situation that generated them.

## 7. Conclusion

k-NN was the best classifier on Titanic (F1 0.72, ROC-AUC 0.85), and MLP was the best regressor on California Housing (R² 0.80). Both results are competitive with published benchmarks on these datasets. Natural next steps would be (i) feature engineering on Titanic (title, family size, cabin letter), (ii) ensemble methods like Random Forest or Gradient Boosting, and (iii) explicit spatial features for California Housing.

## 8. References
- Sehgal, M. *Titanic Data Science Solutions*. Kaggle, https://www.kaggle.com/code/startupsci/titanic-data-science-solutions
- Pace, R. K., & Barry, R. (1997). Sparse spatial autoregressions. *Statistics & Probability Letters*, 33(3), 291–297.
- Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR* 12, 2825–2830.
