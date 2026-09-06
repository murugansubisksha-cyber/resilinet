import os
import sys
import joblib
import pandas as pd
import shap

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)

from preprocessing import FEATURES


MODEL_PATH = "ml/models/risk_model.pkl"


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
        columns=FEATURES,
    )

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(
        input_data
    )

    values = shap_values[0]

    explanation = []

    for feature, value in zip(
        FEATURES,
        values,
    ):

        explanation.append(
            {
                "feature": feature,
                "shap_value": round(
                    float(value),
                    4,
                ),
                "impact": (
                    "increases_risk"
                    if value > 0
                    else "decreases_risk"
                ),
            }
        )

    explanation.sort(
        key=lambda x: abs(
            x["shap_value"]
        ),
        reverse=True,
    )

    return explanation


if __name__ == "__main__":

    sample = {
        "elevation": 1200,
        "slope": 32,
        "road_importance": 5,
        "incident_count": 4,
    }

    result = explain_prediction(sample)

    print("SHAP Explanation")
    print("----------------")

    for item in result:

        print(
            f"{item['feature']:20s} "
            f"{item['shap_value']:>8.4f} "
            f"{item['impact']}"
        )