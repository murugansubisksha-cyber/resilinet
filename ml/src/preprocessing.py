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

TARGET = "risk_score"


def load_data(file_path):
    return pd.read_csv(file_path)


def preprocess_data(file_path):
    df = load_data(file_path)

    required_columns = FEATURES + [TARGET]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    df = df.dropna(
        subset=required_columns
    )

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    return X, y


if __name__ == "__main__":

    X, y = preprocess_data(
        "ml/data/road_risk.csv"
    )

    print("Dataset loaded successfully.")
    print(f"Samples: {len(X)}")
    print(f"Features: {len(FEATURES)}")

    print("\nFeatures:")
    for feature in FEATURES:
        print(f"- {feature}")

    print("\nFirst 5 feature rows:")
    print(X.head())

    print("\nFirst 5 target values:")
    print(y.head())