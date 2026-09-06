# ResiliNet ML Risk Model Handoff

## Model

Model: XGBoost Regressor

Model file:

ml/models/risk_model.pkl

The trained model predicts an engineered road risk score between 0 and 1.

## Prediction Function

The reusable prediction function is:

predict_risk(features: dict)

It returns:

{
    "risk_score": 0.8059,
    "risk_level": "CRITICAL"
}

## Required Features

The model requires exactly these 9 features:

1. rainfall
2. accumulated_rainfall_24h
3. accumulated_rainfall_72h
4. rainfall_intensity
5. weather_severity_index
6. elevation
7. slope
8. road_importance
9. incident_count

## Feature Order

The feature order must remain:

rainfall
accumulated_rainfall_24h
accumulated_rainfall_72h
rainfall_intensity
weather_severity_index
elevation
slope
road_importance
incident_count

## Risk Levels

LOW:

0.00 - 0.24

MEDIUM:

0.25 - 0.49

HIGH:

0.50 - 0.74

CRITICAL:

0.75 - 1.00

## Model Evaluation

MAE: 0.0026

RMSE: 0.0035

R²: 0.9995

These metrics indicate that the XGBoost model closely reproduces the
engineered risk_score on the held-out test set.

The risk_score is an engineered target derived from available
environmental and historical features, so these metrics should not
be interpreted as real-world prediction accuracy.

## SHAP Explainability

SHAP was successfully tested using the trained model.

For the test prediction:

Risk Score: 0.8059

The strongest SHAP contributions were:

- incident_count
- slope
- road_importance
- elevation
- accumulated_rainfall_72h
- rainfall

SHAP provides feature-level contributions explaining why a prediction
is higher or lower.

## Integration

Person 3 can use the predict_risk() function as the ML prediction
layer for the backend risk API.

The backend should provide all 9 required features with the exact
feature names listed above.