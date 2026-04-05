"""
Run live pricing inference for the Host Pricing Assistant project.

This file is responsible for:

1. Loading the saved v1 pricing model artifact
2. Loading the processed training dataset for fallback market estimates
3. Accepting structured listing inputs from the backend
4. Building a one-row DataFrame that matches the training feature schema
5. Running model prediction on the input data
6. Returning a rounded nightly price recommendation
"""

from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "backend" / "app" / "ml" / "artifacts" / "pricing_model.joblib"
TRAINING_DATA_PATH = BASE_DIR / "data" / "processed" / "airbnb_ml_training.csv"


# Load the trained model once so it can be reused for each prediction request.
model = joblib.load(MODEL_PATH)

# Load the processed training dataset once so it can be reused for
# fallback market-price estimation.
training_df = pd.read_csv(TRAINING_DATA_PATH)


def get_fallback_market_price(city: str, property_type: str) -> float:
    """
    Estimate a fallback market price when the user does not provide one.

    The fallback order is:
    1. Same city + property type
    2. Same city
    3. Same property type
    4. Overall dataset average
    """
    city_property_matches = training_df[
        (training_df["city"] == city) &
        (training_df["property_type"] == property_type)
    ]

    if not city_property_matches.empty:
        return float(city_property_matches["nightly_price"].mean())

    city_matches = training_df[training_df["city"] == city]

    if not city_matches.empty:
        return float(city_matches["nightly_price"].mean())

    property_matches = training_df[training_df["property_type"] == property_type]

    if not property_matches.empty:
        return float(property_matches["nightly_price"].mean())

    return float(training_df["nightly_price"].mean())


def predict_price(
    listing_title: str,
    city: str,
    property_type: str,
    beds: int,
    accommodates: int,
    competitor_avg_price: float | None,
) -> tuple[float, float, bool]:
    """
    Predict a nightly price and return metadata about the market price used.

    Returns:
        tuple[float, float, bool]:
        - predicted nightly price
        - market price used for prediction
        - whether a fallback market price was used
    """
    used_fallback = False

    if competitor_avg_price is None:
        competitor_avg_price = get_fallback_market_price(
            city=city,
            property_type=property_type,
        )
        used_fallback = True

    # Build a one-row DataFrame that matches the training feature columns.
    input_df = pd.DataFrame(
        [
            {
                "property_type": property_type,
                "city": city,
                "beds": beds,
                "accommodates": accommodates,
                "competitor_avg_price": competitor_avg_price,
            }
        ]
    )

    # Generate the model prediction.
    prediction = model.predict(input_df)[0]

    return round(float(prediction), 2), round(float(competitor_avg_price), 2), used_fallback