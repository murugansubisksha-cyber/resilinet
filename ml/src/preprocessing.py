import pandas as pd


FEATURES = [
    "rainfall",
    "accumulated_rainfall",
    "elevation",
    "slope",
    "road_importance",
    "historical_incidents",
    "field_evidence",
]

TARGET = "risk_score"


def load_data(file_path):
    """Load the road-risk dataset."""
    return pd.read_csv(file_path)


def validate_columns(df):
    """Check that all required columns are present."""
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


def clean_data(df):
    """Clean and validate the dataset."""

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert required columns to numeric values
    for column in FEATURES + [TARGET]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove rows with missing required values
    df = df.dropna(subset=FEATURES + [TARGET])

    # Remove physically invalid values
    df = df[
        (df["rainfall"] >= 0)
        & (df["accumulated_rainfall"] >= 0)
        & (df["elevation"] >= 0)
        & (df["slope"] >= 0)
        & (df["road_importance"] >= 0)
        & (df["historical_incidents"] >= 0)
        & (df["field_evidence"] >= 0)
        & (df["field_evidence"] <= 1)
        & (df["risk_score"] >= 0)
        & (df["risk_score"] <= 1)
    ]

    return df


def preprocess_data(file_path):
    """Load, validate and preprocess the road-risk dataset."""

    df = load_data(file_path)

    validate_columns(df)

    original_rows = len(df)

    df = clean_data(df)

    removed_rows = original_rows - len(df)

    X = df[FEATURES]
    y = df[TARGET]

    print(f"Original samples: {original_rows}")
    print(f"Removed samples: {removed_rows}")
    print(f"Final samples: {len(X)}")

    return X, y


if __name__ == "__main__":

    X, y = preprocess_data(
        "data/road_risk.csv"
    )

    print("\nDataset preprocessing successful.")
    print(f"Features: {len(FEATURES)}")

    print("\nFeature columns:")
    print(list(X.columns))

    print("\nFirst 5 feature rows:")
    print(X.head())

    print("\nFirst 5 target values:")
    print(y.head())