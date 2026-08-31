import os
import joblib
import pandas as pd

from preprocessing import FEATURES


MODEL_PATH = "models/risk_model.pkl"


def get_risk_level(score):
    score = max(0.0, min(1.0, float(score)))

    if score <= 0.24:
        return "LOW"
    elif score <= 0.49:
        return "MEDIUM"
    elif score <= 0.74:
        return "HIGH"
    else:
        return "CRITICAL"


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Model not found. Run train.py first."
        )

    return joblib.load(MODEL_PATH)


def predict_risk(data):
    missing_features = [
        feature
        for feature in FEATURES
        if feature not in data
    ]

    if missing_features:
        raise ValueError(
            f"Missing features: {missing_features}"
        )

    model = load_model()

    input_data = pd.DataFrame(
        [[data[feature] for feature in FEATURES]],
        columns=FEATURES
    )

    score = float(model.predict(input_data)[0])

    score = max(0.0, min(1.0, score))

    return {
        "risk_score": round(score, 4),
        "risk_level": get_risk_level(score)
    }


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

    result = predict_risk(sample)

    print("Prediction:")
    print(result)