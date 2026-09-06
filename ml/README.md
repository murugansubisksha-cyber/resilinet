# ResiliNet ML - Road Risk Prediction

## Overview

The ResiliNet ML module predicts road risk using weather, terrain, road importance, and historical incident data.

The machine learning pipeline uses **XGBoost Regressor** for risk-score prediction and **SHAP** for model explainability.

The model produces a continuous **risk score between 0 and 1**, which is converted into four risk levels:

- LOW
- MEDIUM
- HIGH
- CRITICAL

## ML Model

- Algorithm: XGBoost Regressor
- Target: `risk_score`
- Output range: `0.0 - 1.0`
- Explainability: SHAP
- Model file: `ml/models/risk_model.pkl`

## Project Structure

```text
ml/
├── data/
├── notebooks/
├── models/
│   └── risk_model.pkl
├── src/
│   ├── preprocessing.py
│   ├── features.py
│   ├── train.py
│   ├── predict.py
│   ├── explain.py
│   ├── risk_service.py
│   ├── test_dynamic_risk.py
│   └── test_risk_service.py
└── README.md