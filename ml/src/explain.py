import os
import joblib
import pandas as pd
import shap

from preprocessing import FEATURES


MODEL_PATH = "models/risk_model.pkl"


def explain_prediction(data):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Model not found. Run train.py first."
        )

    missing_features = [
        feature
        for feature in FEATURES
        if feature not in data
    ]

    if missing_features:
        raise ValueError(
            f"Missing features: {missing_features}"
        )

    model = joblib.load(MODEL_PATH)

    input_data = pd.DataFrame(
        [[data[feature] for feature in FEATURES]],
        columns=FEATURES
    )

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(input_data)

    values = shap_values[0]

    explanation = {}

    for feature, value in zip(FEATURES, values):
        explanation[feature] = round(float(value), 4)

    return explanation


if __name__ == "__main__":
    sample = {
        "rainfall": 180,
        "accumulated_rainfall": 320,
        "elevation": 1200,
        "slope": 32,
        "road_importance": 5,
        "historical_incidents": 4,
        "field_evidence": 0.91,
    }

    result = explain_prediction(sample)

    print("SHAP Explanation:")

    for feature, value in result.items():
        print(f"{feature}: {value}")