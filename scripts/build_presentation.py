"""Build presentation.pptx from the project outline.

Run from project root:
    python scripts/build_presentation.py
Output: report/presentation.pptx
"""
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
OUT = ROOT / "report" / "presentation.pptx"

BLUE = RGBColor(0x1F, 0x3A, 0x68)
DARK = RGBColor(0x22, 0x22, 0x22)
GREY = RGBColor(0x55, 0x55, 0x55)


def add_title_slide(prs, title, subtitle, footer):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    left, top, w, h = Inches(0.7), Inches(1.5), Inches(12.0), Inches(1.6)
    tb = slide.shapes.add_textbox(left, top, w, h)
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = BLUE

    tb2 = slide.shapes.add_textbox(Inches(0.7), Inches(3.2), Inches(12), Inches(1))
    p2 = tb2.text_frame.paragraphs[0]
    p2.text = subtitle
    p2.font.size = Pt(22)
    p2.font.color.rgb = DARK

    tb3 = slide.shapes.add_textbox(Inches(0.7), Inches(6.2), Inches(12), Inches(0.6))
    p3 = tb3.text_frame.paragraphs[0]
    p3.text = footer
    p3.font.size = Pt(14)
    p3.font.color.rgb = GREY
    return slide


def add_header(slide, title):
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.5), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = BLUE


def add_bullets(slide, bullets, left=0.6, top=1.4, width=12.0, height=5.5, size=20):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, text in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text
        p.font.size = Pt(size)
        p.font.color.rgb = DARK
        p.space_after = Pt(8)


def add_image(slide, path, left, top, width=None, height=None):
    if not Path(path).exists():
        return
    kwargs = {}
    if width is not None:
        kwargs["width"] = Inches(width)
    if height is not None:
        kwargs["height"] = Inches(height)
    slide.shapes.add_picture(str(path), Inches(left), Inches(top), **kwargs)


def add_table(slide, headers, rows, left, top, width, height, header_fill=BLUE):
    ncols = len(headers)
    nrows = len(rows) + 1
    tbl = slide.shapes.add_table(nrows, ncols,
                                 Inches(left), Inches(top),
                                 Inches(width), Inches(height)).table
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_fill
        for p in cell.text_frame.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                r.font.size = Pt(14)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(13)
                    r.font.color.rgb = DARK
    return tbl


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Slide 1 — title
    add_title_slide(
        prs,
        title="Applied Machine Learning with scikit-learn",
        subtitle="Comparing classifiers and regressors across two datasets",
        footer="Tanay Malavia  •  CSCI 164  •  Spring 2026  •  github.com/malaviatanay/Applied-Machine-Learning-with-scikit-learn",
    )

    # Slide 2 — problem & goals
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s, "Problem & Goals")
    add_bullets(s, [
        "• Build the full supervised-learning pipeline on two real datasets",
        "• Apply three algorithms per dataset, tune them, compare results",
        "• Benchmark against prior published work",
        "• Deliverables: Jupyter notebooks, summary report, presentation",
    ])

    # Slide 3 — datasets
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s, "Datasets")
    add_table(
        s,
        headers=["Dataset", "Task", "Size", "Target"],
        rows=[
            ["Titanic", "Classification", "891 rows, 11 features", "Survived (0/1)"],
            ["California Housing", "Regression", "20,640 rows, 8 features", "MedHouseVal ($100k)"],
        ],
        left=0.6, top=1.6, width=12.0, height=1.5,
    )
    add_bullets(s, [
        "• Why these: small, well-documented, strong prior-work benchmarks",
        "• Cover both classification and regression",
    ], top=4.0, size=20)
    add_image(s, FIG / "ca_geo.png", left=8.2, top=4.6, width=4.8)

    # Slide 4 — preprocessing
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s, "Preprocessing")
    add_bullets(s, [
        "Titanic",
        "  • Dropped PassengerId / Name / Ticket / Cabin",
        "  • Imputed Age (median), Embarked (mode)",
        "  • One-hot encoded Sex, Embarked",
        "  • Scaled numeric features",
        "",
        "California Housing",
        "  • No missing values",
        "  • StandardScaler for linear / MLP models",
        "",
        "Validation: 80/20 train-test split, 5-fold CV on training data",
    ], size=18)

    # Slide 5 — models
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s, "Models & Rationale")
    add_table(
        s,
        headers=["Dataset", "Models"],
        rows=[
            ["Titanic", "Logistic Regression  •  k-NN  •  Decision Tree"],
            ["California Housing", "Linear Regression  •  Decision Tree  •  MLP"],
        ],
        left=0.6, top=1.6, width=12.0, height=1.5,
    )
    add_bullets(s, [
        "• Linear / Logistic → interpretable baseline",
        "• k-NN / Decision Tree → non-parametric, capture local and non-linear structure",
        "• MLP → flexible non-linear fit for continuous target",
        "",
        "Tuning: GridSearchCV over C, k, max_depth, hidden_layer_sizes, alpha",
    ], top=3.6, size=18)

    # Slide 6 — Titanic results
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s, "Results — Titanic (Classification)")
    add_table(
        s,
        headers=["Model", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
        rows=[
            ["LogReg", "0.7933", "0.7759", "0.6522", "0.7087", "0.8472"],
            ["k-NN  (winner)", "0.7989", "0.7797", "0.6667", "0.7188", "0.8489"],
            ["Tree", "0.7877", "0.8163", "0.5797", "0.6780", "0.7827"],
        ],
        left=0.6, top=1.4, width=7.2, height=1.8,
    )
    add_bullets(s, [
        "• k-NN wins overall — highest F1 and ROC-AUC",
        "• Tree has best precision (0.82) but worst recall (0.58)",
        "  → over-conservative decision boundary",
    ], top=3.6, size=18, width=7.5)
    add_image(s, FIG / "titanic_roc.png", left=8.3, top=1.4, width=4.8)

    # Slide 7 — California results
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s, "Results — California Housing (Regression)")
    add_table(
        s,
        headers=["Model", "MAE", "RMSE", "R^2"],
        rows=[
            ["Linear", "0.5332", "0.7456", "0.5758"],
            ["Tree", "0.4041", "0.5979", "0.7272"],
            ["MLP  (winner)", "0.3448", "0.5100", "0.8015"],
        ],
        left=0.6, top=1.4, width=7.2, height=1.8,
    )
    add_bullets(s, [
        "• MLP wins — R^2 0.80, beats Linear by 24 points",
        "• Linear underfits: income → value is non-linear",
        "• Tree intermediate: axis-aligned greedy splits",
    ], top=3.6, size=18, width=7.5)
    add_image(s, FIG / "ca_pred_vs_actual.png", left=8.3, top=1.4, width=4.8)

    # Slide 8 — prior work
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s, "Comparison to Prior Work")
    add_bullets(s, [
        "Titanic — Sehgal (Kaggle): reports 0.77–0.84 accuracy",
        "  → Our 0.79 sits mid-band",
        "  → Gap = feature engineering we omitted (titles, family size)",
        "",
        "California Housing — Pace & Barry (1997): R^2 ≈ 0.65 (spatial autoregression)",
        "  → Our MLP: 0.80, matching modern sklearn benchmarks",
        "  → MLP captures the non-linear income-to-value curve",
    ], size=18)

    # Slide 9 — lessons
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s, "Lessons & Limitations")
    add_bullets(s, [
        "What worked",
        "  • Pipelines kept CV leakage-free",
        "  • GridSearchCV materially improved Tree and MLP",
        "",
        "Limitations",
        "  • Titanic test set ~178 rows → 1–2 point gaps are noise",
        "  • CA target capped at $500k → residual spike at high end",
        "  • No ensemble methods (out of scope per rubric)",
        "",
        "Next steps: feature engineering, gradient boosting, spatial features",
    ], size=18)

    # Slide 10 — thanks
    s = prs.slides.add_slide(prs.slide_layouts[6])
    tb = s.shapes.add_textbox(Inches(0.7), Inches(2.8), Inches(12), Inches(1.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "Thanks — Questions?"
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = BLUE
    p.alignment = PP_ALIGN.CENTER

    tb2 = s.shapes.add_textbox(Inches(0.7), Inches(4.6), Inches(12), Inches(1))
    p2 = tb2.text_frame.paragraphs[0]
    p2.text = "github.com/malaviatanay/Applied-Machine-Learning-with-scikit-learn"
    p2.font.size = Pt(20)
    p2.font.color.rgb = GREY
    p2.alignment = PP_ALIGN.CENTER

    prs.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
