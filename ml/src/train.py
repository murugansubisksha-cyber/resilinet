import os
import sys
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from xgboost import XGBRegressor

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from preprocessing import preprocess_data, FEATURES


DATA_PATH = "ml/data/road_risk.csv"
MODEL_PATH = "ml/models/risk_model.pkl"


def train_model():

    print("Loading dataset...")

    X, y = preprocess_data(
        DATA_PATH
    )

    print(
        f"Total samples: {len(X)}"
    )

    print(
        f"Features: {len(FEATURES)}"
    )

    print("\nSplitting dataset...")

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
        )
    )

    print(
        f"Training samples: {len(X_train)}"
    )

    print(
        f"Testing samples: {len(X_test)}"
    )

    print("\nTraining XGBoost model...")

    model = XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        X_train,
        y_train,
    )

    print("Training completed.")

    print("\nEvaluating model...")

    predictions = model.predict(
        X_test
    )

    predictions = predictions.clip(
        0,
        1,
    )

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = mean_squared_error(
        y_test,
        predictions,
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions,
    )

    print(
        f"MAE  : {mae:.4f}"
    )

    print(
        f"RMSE : {rmse:.4f}"
    )

    print(
        f"R²   : {r2:.4f}"
    )

    print("\nFeature Importance:")

    importance = model.feature_importances_

    feature_importance = sorted(
        zip(
            FEATURES,
            importance,
        ),
        key=lambda x: x[1],
        reverse=True,
    )

    for feature, value in feature_importance:
        print(
            f"{feature:35s} {value:.4f}"
        )

    # Create model directory
    os.makedirs(
        os.path.dirname(MODEL_PATH),
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print(
        f"\nModel saved to: {MODEL_PATH}"
    )

    return model


if __name__ == "__main__":
    train_model()