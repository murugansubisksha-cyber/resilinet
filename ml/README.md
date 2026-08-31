# ResiliNet ML Engine

## Person 4 - Road Risk Prediction

This module predicts road hazard risk using machine learning and provides explainable risk predictions.

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- SHAP
- Joblib

## Features

The model uses the following features:

- Rainfall
- Accumulated rainfall
- Elevation
- Slope
- Road importance
- Historical incidents
- Field evidence

## Risk Levels

| Score | Level |
|---|---|
| 0.00 - 0.24 | LOW |
| 0.25 - 0.49 | MEDIUM |
| 0.50 - 0.74 | HIGH |
| 0.75 - 1.00 | CRITICAL |

## Files

- `preprocessing.py` - Loads, validates, and preprocesses the dataset
- `train.py` - Trains the XGBoost risk prediction model
- `predict.py` - Generates risk scores and risk levels
- `explain.py` - Generates SHAP-based feature explanations

## Dataset

The training dataset should be placed at:

```text
data/road_risk.csv