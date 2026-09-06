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
    """
    Convert numerical risk score into a risk category.
    """
    if risk_score <= 0.24:
        return "LOW"
    elif risk_score <= 0.49:
        return "MEDIUM"
    elif risk_score <= 0.74:
        return "HIGH"
    else:
        return "CRITICAL"


def validate_features(features):
    """
    Validate the input feature dictionary.
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

    for feature in FEATURES:
        value = features[feature]

        if value is None:
            raise ValueError(
                f"Feature '{feature}' cannot be None"
            )

        try:
            float(value)
        except (TypeError, ValueError):
            raise ValueError(
                f"Feature '{feature}' must be numeric"
            )

    return True


def load_model():
    """
    Load the trained XGBoost model.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def predict_risk(features):
    """
    Predict road risk using the trained XGBoost model.

    Parameters
    ----------
    features : dict
        Dictionary containing all 9 required features.

    Returns
    -------
    dict
        Risk score and risk level.
    """

    validate_features(features)

    model = load_model()

    input_data = {
        feature: float(features[feature])
        for feature in FEATURES
    }

    dataframe = pd.DataFrame(
        [input_data],
        columns=FEATURES
    )

    prediction = model.predict(dataframe)

    risk_score = float(prediction[0])

    # Keep score within valid range.
    risk_score = max(0.0, min(1.0, risk_score))

    return {
        "risk_score": round(risk_score, 4),
        "risk_level": get_risk_level(risk_score),
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

    print("Risk Prediction")
    print("----------------")
    print(f"Risk Score : {result['risk_score']}")
    print(f"Risk Level : {result['risk_level']}")