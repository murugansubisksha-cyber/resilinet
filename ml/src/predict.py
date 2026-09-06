import os
import sys
import joblib
import pandas as pd


sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from preprocessing import FEATURES


MODEL_PATH = "ml/models/risk_model.pkl"


def get_risk_level(score):

    score = max(
        0.0,
        min(1.0, float(score))
    )

    if score <= 0.24:
        return "LOW"

    elif score <= 0.49:
        return "MEDIUM"

    elif score <= 0.74:
        return "HIGH"

    else:
        return "CRITICAL"


def load_model():

    if not os.path.exists(
        MODEL_PATH
    ):
        raise FileNotFoundError(
            "Model not found. Run train.py first."
        )

    return joblib.load(
        MODEL_PATH
    )


def get_factor_level(
    value,
    low,
    medium,
    high,
):

    if value < low:
        return "LOW"

    elif value < medium:
        return "MEDIUM"

    elif value < high:
        return "HIGH"

    else:
        return "CRITICAL"


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
        [
            [
                data[feature]
                for feature in FEATURES
            ]
        ],
        columns=FEATURES,
    )

    score = float(
        model.predict(
            input_data
        )[0]
    )

    score = max(
        0.0,
        min(1.0, score)
    )

    factors = {

        "rainfall": get_factor_level(
            float(data["rainfall"]),
            50,
            150,
            250,
        ),

        "slope": get_factor_level(
            float(data["slope"]),
            10,
            20,
            27,
        ),

        "elevation": get_factor_level(
            float(data["elevation"]),
            375,
            410,
            440,
        ),

        "road_importance": get_factor_level(
            float(data["road_importance"]),
            2,
            4,
            5,
        ),

        "historical_incidents": get_factor_level(
            float(data["incident_count"]),
            1,
            3,
            5,
        ),

        "weather_severity": get_factor_level(
            float(data["weather_severity_index"]),
            0.30,
            0.60,
            0.80,
        ),
    }

    return {
        "risk_score": round(
            score,
            4,
        ),

        "risk_level": get_risk_level(
            score
        ),

        "factors": factors,
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

    result = predict_risk(
        sample
    )

    print("Prediction")
    print("----------")

    print(
        f"Risk Score : {result['risk_score']}"
    )

    print(
        f"Risk Level : {result['risk_level']}"
    )

    print("\nRisk Factors")
    print("------------")

    for feature, level in result[
        "factors"
    ].items():

        print(
            f"{feature}: {level}"
        )