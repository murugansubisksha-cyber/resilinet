from pathlib import Path

import joblib
import pandas as pd
import shap


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


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def validate_features(features):
    if not isinstance(features, dict):
        raise TypeError("features must be a dictionary")

    missing_features = [
        feature
        for feature in FEATURES
        if feature not in features
    ]

    if missing_features:
        raise ValueError(
            f"Missing features: {missing_features}"
        )

    try:
        numeric_features = {
            feature: float(features[feature])
            for feature in FEATURES
        }
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "All feature values must be numeric."
        ) from exc

    return numeric_features


def explain_prediction(features):
    """
    Generate SHAP feature contributions for one prediction.

    Returns:
        Dictionary containing:
        - prediction
        - feature_importance
    """

    numeric_features = validate_features(features)

    model = load_model()

    input_data = pd.DataFrame(
        [
            [
                numeric_features[feature]
                for feature in FEATURES
            ]
        ],
        columns=FEATURES,
    )

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(input_data)

    if hasattr(shap_values, "values"):
        values = shap_values.values
    else:
        values = shap_values

    if hasattr(values, "ndim") and values.ndim > 1:
        values = values[0]

    values = list(values)

    prediction = float(model.predict(input_data)[0])

    contributions = {}

    for feature, value in zip(FEATURES, values):
        contributions[feature] = float(value)

    sorted_contributions = dict(
        sorted(
            contributions.items(),
            key=lambda item: abs(item[1]),
            reverse=True,
        )
    )

    return {
        "prediction": prediction,
        "feature_importance": sorted_contributions,
    }


if __name__ == "__main__":

    sample = {
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
        result = explain_prediction(sample)

        print("SHAP RISK EXPLANATION")
        print()
        print(f"Predicted Risk Score: {result['prediction']:.4f}")

        print()
        print("Feature Contributions:")
        print("-" * 60)

        for feature, contribution in result[
            "feature_importance"
        ].items():

            direction = (
                "increases risk"
                if contribution > 0
                else "decreases risk"
            )

            print(
                f"{feature:35s} "
                f"{contribution:+.6f} "
                f"({direction})"
            )

        print()
        print("SHAP explanation completed successfully.")

    except Exception as error:
        print()
        print("SHAP explanation failed.")
        print(f"Error: {error}")
        raise