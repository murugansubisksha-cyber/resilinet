from pathlib import Path
import joblib
import pandas as pd

FEATURES = [
    "rainfall",
    "accumulated_rainfall_24h",
    "accumulated_rainfall_72h",
    "rainfall_intensity",
    "weather_severity_index",
    "elevation",
    "slope",
    "road_importance",
    "incident_count",
]

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "risk_model.pkl"


def get_risk_level(risk_score):
    if risk_score <= 0.24:
        return "LOW"
    elif risk_score <= 0.49:
        return "MEDIUM"
    elif risk_score <= 0.74:
        return "HIGH"
    else:
        return "CRITICAL"


def predict_risk(features: dict) -> dict:
    """
    Predict road risk from the required ML features.

    Returns:
        {
            "risk_score": float,
            "risk_level": str
        }
    """

    if not isinstance(features, dict):
        raise TypeError("features must be a dictionary")

    missing_features = [
        feature for feature in FEATURES
        if feature not in features
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    try:
        input_data = {
            feature: float(features[feature])
            for feature in FEATURES
        }
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "All feature values must be numeric"
        ) from exc

    model = joblib.load(MODEL_PATH)

    input_df = pd.DataFrame(
        [[input_data[feature] for feature in FEATURES]],
        columns=FEATURES
    )

    prediction = float(model.predict(input_df)[0])

    # Keep the score within the required 0-1 range.
    risk_score = max(0.0, min(1.0, prediction))

    return {
        "risk_score": round(risk_score, 4),
        "risk_level": get_risk_level(risk_score)
    }


if __name__ == "__main__":
    sample_features = {
        "rainfall": 220,
        "accumulated_rainfall_24h": 220,
        "accumulated_rainfall_72h": 220,
        "rainfall_intensity": 220,
        "weather_severity_index": 0.82,
        "elevation": 420,
        "slope": 25,
        "road_importance": 5,
        "incident_count": 4,
    }

    result = predict_risk(sample_features)

    print("Risk prediction successful.")
    print(f"Risk Score: {result['risk_score']}")
    print(f"Risk Level: {result['risk_level']}")