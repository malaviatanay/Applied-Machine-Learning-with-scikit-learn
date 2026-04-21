# Presentation Outline — CSCI 164 Final Project
10 minutes • 10 slides • ~1 min per slide

Copy each slide's content into Google Slides / PowerPoint / Keynote. Numbers and bullet points kept tight so you can speak to them rather than read them.

---

## Slide 1 — Title

**Applied Machine Learning with scikit-learn**
Comparing classifiers and regressors across two datasets

Tanay Malavia • CSCI 164 • Spring 2026
GitHub: `github.com/malaviatanay/Applied-Machine-Learning-with-scikit-learn`

**Speaker notes:** Brief hello; this project is about building and comparing classical ML models on two datasets end-to-end.

---

## Slide 2 — Problem & Goals

- Build the full supervised-learning pipeline on **two real datasets**
- Apply **three algorithms** per dataset, tune them, compare
- Benchmark results against **prior published work**
- Deliverables: notebooks, report, presentation

**Speaker notes:** The goal isn't just accuracy — it's demonstrating the whole workflow: EDA → preprocessing → modeling → tuning → evaluation → literature comparison.

---

## Slide 3 — Datasets

| Dataset              | Task           | Size            | Target         |
|----------------------|----------------|-----------------|----------------|
| Titanic              | Classification | 891 rows, 11 feat | `Survived` (0/1) |
| California Housing   | Regression     | 20,640 rows, 8 feat | `MedHouseVal` ($100k) |

**Why these:** small enough to iterate fast, well-documented, strong prior-work benchmarks.

**Speaker notes:** Titanic covers classification with mixed feature types; CA Housing covers regression on numeric features with geographic structure.

---

## Slide 4 — Preprocessing

**Titanic:**
- Dropped `PassengerId`, `Name`, `Ticket`, `Cabin`
- Imputed `Age` (median), `Embarked` (mode)
- One-hot encoded `Sex`, `Embarked`
- Scaled numeric features

**California Housing:**
- No missing values
- StandardScaler for linear / MLP models
- 80/20 train/test split, 5-fold CV on train

**Speaker notes:** Each pipeline was wrapped in a `ColumnTransformer` + `Pipeline` so scaling happens inside each CV fold (no leakage).

---

## Slide 5 — Models & Why

| Dataset    | Models                                               |
|------------|------------------------------------------------------|
| Titanic    | Logistic Regression, k-NN, Decision Tree             |
| CA Housing | Linear Regression, Decision Tree, MLP                |

- **Linear / Logistic** → interpretable baseline
- **k-NN / Decision Tree** → non-parametric, captures local & non-linear structure
- **MLP** → flexible non-linear fit for continuous target

Tuning: `GridSearchCV` over C, k, `max_depth`, `hidden_layer_sizes`, alpha.

---

## Slide 6 — Results: Titanic

| Model  | Accuracy | F1     | ROC-AUC |
|--------|----------|--------|---------|
| LogReg | 0.7933   | 0.7087 | 0.8472  |
| **kNN**    | **0.7989**   | **0.7188** | **0.8489**  |
| Tree   | 0.7877   | 0.6780 | 0.7827  |

**Winner: k-NN** — best F1 and ROC-AUC.
Tree has highest precision (0.82) but lowest recall (0.58) — over-conservative.

*Show confusion matrices + ROC curves image on this slide (figures/titanic_confusion.png, titanic_roc.png).*

---

## Slide 7 — Results: California Housing

| Model  | MAE    | RMSE   | R²     |
|--------|--------|--------|--------|
| Linear | 0.5332 | 0.7456 | 0.5758 |
| Tree   | 0.4041 | 0.5979 | 0.7272 |
| **MLP**    | **0.3448** | **0.5100** | **0.8015** |

**Winner: MLP** — R² 0.80, beating linear by 24 points.
Linear underfits because income→value is non-linear.

*Show predicted-vs-actual scatter (figures/ca_pred_vs_actual.png).*

---

## Slide 8 — Comparison to Prior Work

**Titanic** — Sehgal's Kaggle notebook reports 0.77–0.84 accuracy
→ Our 0.79 sits in the middle. Gap explained by feature engineering we omitted (title, family size).

**California Housing** — Pace & Barry (1997): R² ≈ 0.65 with spatial autoregression
→ Our MLP: **0.80**, matching modern sklearn benchmarks.

**Speaker notes:** Our MLP substantially exceeds the original paper, mainly because the MLP can capture the non-linear income-to-value curve directly.

---

## Slide 9 — Lessons & Limitations

**What worked:**
- Wrapping preprocessing in pipelines — clean CV, no leakage
- GridSearchCV surfaced meaningful improvements on Tree and MLP

**Limitations:**
- Titanic test set only ~178 rows → 1–2 point metric gaps are noise
- CA target capped at $500k → residual spike at high end
- No ensemble methods (out of scope per rubric)

**Next steps:** feature engineering (Titanic titles), gradient boosting, spatial features.

---

## Slide 10 — Thanks / Q&A

**Thanks! Questions?**

Repo: `github.com/malaviatanay/Applied-Machine-Learning-with-scikit-learn`

*Keep one backup slide with confusion matrix / residual plot in case someone asks for detail.*

---

## Timing plan (10 min)
- 1–2: 1 min (intro)
- 3–5: 3 min (datasets, preprocessing, models)
- 6–7: 3 min (results)
- 8: 1 min (prior work)
- 9: 1 min (lessons)
- 10: 1 min (Q&A buffer)

## Images to include (all in `figures/`)
- Slide 3 or 4: `ca_geo.png` (eye-catching color map)
- Slide 6: `titanic_confusion.png`, `titanic_roc.png`
- Slide 7: `ca_pred_vs_actual.png`, `ca_residuals.png`
