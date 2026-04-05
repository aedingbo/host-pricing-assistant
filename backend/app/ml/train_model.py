"""
Train the v1 pricing model for the Host Pricing Assistant project.

This file is responsible for:

1. Loading the processed training dataset
2. Selecting the structured v1 regression features
3. Splitting the data into training and test sets
4. Building preprocessing for categorical and numeric columns
5. Training a Linear Regression model
6. Training a Ridge Regression model
7. Comparing model performance with MAE, RMSE, and R^2
8. Saving the best-performing model artifact for inference
"""

from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


BASE_DIR = Path(__file__).resolve().parents[3]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
ARTIFACTS_DIR = BASE_DIR / "backend" / "app" / "ml" / "artifacts"

TRAIN_FILE_PATH = PROCESSED_DIR / "airbnb_ml_training.csv"
BEST_MODEL_PATH = ARTIFACTS_DIR / "pricing_model.joblib"
METRICS_PATH = ARTIFACTS_DIR / "model_metrics.csv"


def evaluate_model(
    model_name: str,
    pipeline: Pipeline,
    x_train: pd.DataFrame,
    x_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> dict:
    # Fit the pipeline on the training data.
    pipeline.fit(x_train, y_train)

    # Generate predictions on the test data.
    predictions = pipeline.predict(x_test)

    # Calculate evaluation metrics.
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    return {
        "model_name": model_name,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "pipeline": pipeline,
    }


def main() -> None:
    # Create the artifacts folder if it does not exist.
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load the processed training dataset.
    df = pd.read_csv(TRAIN_FILE_PATH)

    # Select the structured v1 model features.
    feature_columns = [
        "property_type",
        "city",
        "beds",
        "accommodates",
        "competitor_avg_price",
    ]

    target_column = "nightly_price"

    # Create X and y for supervised regression.
    x = df[feature_columns].copy()
    y = df[target_column].copy()

    # Split the dataset into training and test sets.
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
    )

    # Define categorical and numeric feature groups.
    categorical_features = ["property_type", "city"]
    numeric_features = ["beds", "accommodates", "competitor_avg_price"]

    # Build preprocessing for the regression pipelines.
    preprocessing = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
            (
                "numeric",
                "passthrough",
                numeric_features,
            ),
        ]
    )

    # Build the Linear Regression pipeline.
    linear_pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("model", LinearRegression()),
        ]
    )

    # Build the Ridge Regression pipeline.
    ridge_pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("model", Ridge(alpha=1.0)),
        ]
    )

    # Train and evaluate both models.
    linear_results = evaluate_model(
        model_name="LinearRegression",
        pipeline=linear_pipeline,
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
    )

    ridge_results = evaluate_model(
        model_name="RidgeRegression",
        pipeline=ridge_pipeline,
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
    )

    results = [linear_results, ridge_results]

    # Convert metrics into a DataFrame for easy comparison and export.
    metrics_df = pd.DataFrame(
        [
            {
                "model_name": result["model_name"],
                "mae": result["mae"],
                "rmse": result["rmse"],
                "r2": result["r2"],
            }
            for result in results
        ]
    )

    # Choose the best model using lowest RMSE.
    best_result = min(results, key=lambda result: result["rmse"])
    best_pipeline = best_result["pipeline"]

    # Save metrics and the best model artifact.
    metrics_df.to_csv(METRICS_PATH, index=False)
    joblib.dump(best_pipeline, BEST_MODEL_PATH)

    print("\nTRAINING DATASET SHAPE")
    print(df.shape)

    print("\nFEATURE COLUMNS USED FOR V1 MODEL")
    print(feature_columns)

    print("\nTARGET COLUMN")
    print(target_column)

    print("\nMODEL COMPARISON")
    print(metrics_df)

    print("\nBEST MODEL")
    print(best_result["model_name"])

    print("\nBEST MODEL RMSE")
    print(best_result["rmse"])

    print("\nMODEL ARTIFACT PATH")
    print(BEST_MODEL_PATH)

    print("\nMETRICS OUTPUT PATH")
    print(METRICS_PATH)


if __name__ == "__main__":
    main()