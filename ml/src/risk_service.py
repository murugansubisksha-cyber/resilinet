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

MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "models"
    / "risk_model.pkl"
)


def get_risk_level(risk_score: float) -> str:
    """
    Convert a model risk score in the range 0-1
    into the application's risk category.
    """
    if risk_score <= 0.24:
        return "LOW"
    elif risk_score <= 0.49:
        return "MEDIUM"
    elif risk_score <= 0.74:
        return "HIGH"
    else:
        return "CRITICAL"


def validate_features(features: dict) -> None:
    """
    Validate that all required ML features are present
    and contain numeric values.
    """
    if not isinstance(features, dict):
        raise TypeError("features must be a dictionary")

    missing_features = [
        feature
        for feature in FEATURES
        if feature not in features
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    for feature in FEATURES:
        try:
            float(features[feature])
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Feature '{feature}' must be numeric"
            ) from exc


def load_model():
    """
    Load the trained XGBoost model.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Risk model not found at: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def predict_risk(features: dict) -> dict:
    """
    Predict road risk using the trained XGBoost model.

    Parameters
    ----------
    features : dict
        Dictionary containing all 9 required ML features.

    Returns
    -------
    dict
        risk_score and risk_level.
    """

    validate_features(features)

    input_data = {
        feature: float(features[feature])
        for feature in FEATURES
    }

    model = load_model()

    input_df = pd.DataFrame(
        [[input_data[feature] for feature in FEATURES]],
        columns=FEATURES,
    )

    prediction = float(model.predict(input_df)[0])

    # Keep the score within the expected 0-1 range.
    risk_score = max(0.0, min(1.0, prediction))

    risk_level = get_risk_level(risk_score)

    return {
        "risk_score": round(risk_score, 4),
        "risk_level": risk_level,
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

    try:
        result = predict_risk(sample_features)

        print("Risk prediction successful.")
        print(f"Risk Score: {result['risk_score']}")
        print(f"Risk Level: {result['risk_level']}")

    except Exception as exc:
        print(f"Risk prediction failed: {exc}")