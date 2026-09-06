# ResiliNet ML Risk Model Handoff

## 1. ML Component

The ResiliNet ML module provides road-risk prediction using a trained XGBoost regression model.

Model file:

`ml/models/risk_model.pkl`

Prediction service:

`ml/src/risk_service.py`

The backend should use `predict_risk()` from `risk_service.py` as the standard ML prediction interface.

---

## 2. Model Input

The model requires exactly 9 features:

1. rainfall
2. accumulated_rainfall_24h
3. accumulated_rainfall_72h
4. rainfall_intensity
5. weather_severity_index
6. elevation
7. slope
8. road_importance
9. incident_count

All feature values must be numeric.

---

## 3. Input Example

```json
{
  "rainfall": 220,
  "accumulated_rainfall_24h": 220,
  "accumulated_rainfall_72h": 220,
  "rainfall_intensity": 220,
  "weather_severity_index": 0.82,
  "elevation": 420,
  "slope": 25,
  "road_importance": 5,
  "incident_count": 4
}