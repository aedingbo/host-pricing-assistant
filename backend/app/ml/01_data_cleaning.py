"""
Clean the raw Airbnb pricing dataset.

This file is responsible for:

1. Loading the raw Airbnb-style CSV file
2. Parsing property type and location information from the Title column
3. Mapping the Detail column into the listing_title field
4. Extracting a numeric beds field from the Number of bed column
5. Deriving accommodates from the beds field
6. Converting the main price field into the nightly_price target
7. Dropping rows with missing nightly_price
8. Standardizing raw property types into a cleaned project taxonomy
9. Creating a training-time market anchor for the competitorAvgPrice concept
10. Exporting processed datasets while preserving preview/debug output
"""

import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[3]
RAW_FILE_PATH = BASE_DIR / "data" / "raw" / "airnb.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
TRAIN_OUTPUT_PATH = PROCESSED_DIR / "airbnb_ml_training.csv"
DEMO_OUTPUT_PATH = PROCESSED_DIR / "airbnb_demo_sample.csv"


def parse_title(value: str) -> tuple[str | None, str | None, str | None, str | None]:
    # Return missing values if the title is missing.
    if pd.isna(value):
        return None, None, None, None

    value = str(value).strip()

    # Split the field into property type and location text.
    if " in " in value:
        property_type, location = value.split(" in ", 1)
    else:
        return value, None, None, None

    # Split the location into parts.
    parts = [part.strip() for part in location.split(",")]

    city = parts[0] if len(parts) >= 1 else None
    region = parts[1] if len(parts) >= 3 else None
    country = parts[-1] if len(parts) >= 2 else None

    return property_type, city, region, country


def extract_beds(value: str) -> float:
    # Return missing if the bed field is missing.
    if pd.isna(value):
        return pd.NA

    match = re.search(r"(\d+)", str(value))

    if match:
        return float(match.group(1))

    return pd.NA


def standardize_property_type(value: str) -> str:
    # Return other if the raw property type is missing.
    if pd.isna(value):
        return "other"

    value = str(value).strip().lower()

    if value == "apartment":
        return "apartment"

    if value in {"home", "vacation home", "townhouse"}:
        return "house"

    if value == "cabin":
        return "cabin"

    if value == "condo":
        return "condo"

    if value == "room":
        return "room"

    if value == "villa":
        return "villa"

    if value == "tiny home":
        return "tiny_home"

    if value == "treehouse":
        return "treehouse"

    if value == "cottage":
        return "cottage"

    if value == "guesthouse":
        return "guesthouse"

    if value == "loft":
        return "loft"

    if value == "farm stay":
        return "farm_stay"

    if value == "guest suite":
        return "guest_suite"

    if value == "bungalow":
        return "bungalow"

    if value == "chalet":
        return "chalet"

    if value in {"hotel", "hotel room", "boutique hotel", "hostel", "resort"}:
        return "hotel"

    if value in {
        "dome",
        "hut",
        "tent",
        "yurt",
        "camper/rv",
        "campsite",
        "shepherd’s hut",
        "nature lodge",
        "shipping container",
        "barn",
        "earthen home",
        "castle",
        "lighthouse",
        "cave",
        "tower",
        "windmill",
        "trullo",
        "island",
        "boat",
        "houseboat",
    }:
        return "unique_stay"

    if value == "place to stay":
        return "other"

    return "other"


def add_competitor_avg_price(df: pd.DataFrame) -> pd.DataFrame:
    # Build fallback averages for the market anchor feature.
    city_property_mean = df.groupby(["city", "property_type"])["nightly_price"].transform("mean")
    city_mean = df.groupby("city")["nightly_price"].transform("mean")
    property_mean = df.groupby("property_type")["nightly_price"].transform("mean")
    overall_mean = df["nightly_price"].mean()

    # Prefer city + property_type, then city, then property_type, then overall.
    df["competitor_avg_price"] = city_property_mean
    df["competitor_avg_price"] = df["competitor_avg_price"].fillna(city_mean)
    df["competitor_avg_price"] = df["competitor_avg_price"].fillna(property_mean)
    df["competitor_avg_price"] = df["competitor_avg_price"].fillna(overall_mean)

    return df


def main() -> None:
    # Create the processed output folder if needed.
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Load the raw CSV file into a DataFrame.
    df = pd.read_csv(RAW_FILE_PATH)

    # Create listing_title from the Detail column.
    df["listing_title"] = df["Detail"].astype(str).str.strip()

    # Parse Title into structured fields.
    parsed_title = df["Title"].apply(parse_title)
    df[["property_type_raw", "city", "region", "country"]] = pd.DataFrame(
        parsed_title.tolist(),
        index=df.index,
    )

    # Create the standardized property type field.
    df["property_type"] = df["property_type_raw"].apply(standardize_property_type)

    # Extract a numeric beds field from the Number of bed column.
    df["beds"] = df["Number of bed"].apply(extract_beds)

    # Derive accommodates using the business rule.
    df["accommodates"] = df["beds"] * 2

    # Convert the main price column into the nightly_price target.
    df["nightly_price"] = pd.to_numeric(
        df["Price(in dollar)"],
        errors="coerce",
    )

    # Drop rows where the target is missing.
    before_drop = len(df)
    df = df.dropna(subset=["nightly_price"]).copy()
    after_drop = len(df)
    dropped_rows = before_drop - after_drop

    # Add the training-time market anchor feature.
    df = add_competitor_avg_price(df)

    cleaned_columns = [
        "listing_title",
        "property_type_raw",
        "property_type",
        "city",
        "region",
        "country",
        "beds",
        "accommodates",
        "competitor_avg_price",
        "nightly_price",
    ]

    model_columns_v1 = [
        "listing_title",
        "property_type",
        "city",
        "beds",
        "accommodates",
        "competitor_avg_price",
        "nightly_price",
    ]

    # Create export datasets.
    df_training = df[model_columns_v1].copy()
    df_demo = df[cleaned_columns].sample(
        n=min(50, len(df)),
        random_state=42,
    ).copy()

    # Export processed datasets.
    df_training.to_csv(TRAIN_OUTPUT_PATH, index=False)
    df_demo.to_csv(DEMO_OUTPUT_PATH, index=False)

    print("\nROWS DROPPED FOR MISSING TARGET")
    print(dropped_rows)

    print("\nSTANDARDIZED PROPERTY TYPE COUNTS")
    print(df["property_type"].value_counts().sort_values(ascending=False))

    print("\nRAW TO STANDARDIZED PROPERTY TYPE SAMPLE")
    print(
        df[["property_type_raw", "property_type"]]
        .drop_duplicates()
        .sort_values(["property_type", "property_type_raw"])
        .to_string(index=False)
    )

    print("\nCLEANED DATA PREVIEW")
    print(df[cleaned_columns].head(10))

    print("\nCLEANED MISSING VALUES")
    print(df[cleaned_columns].isna().sum())

    print("\nV1 MODEL COLUMNS")
    print(model_columns_v1)

    print("\nNOT USED AS V1 MODEL FEATURES")
    print(["region", "country", "property_type_raw"])

    print("\nCOMPETITOR AVG PRICE SUMMARY")
    print(df["competitor_avg_price"].describe())

    print("\nTRAINING DATASET SHAPE")
    print(df_training.shape)

    print("\nTRAINING DATASET OUTPUT PATH")
    print(TRAIN_OUTPUT_PATH)

    print("\nDEMO DATASET OUTPUT PATH")
    print(DEMO_OUTPUT_PATH)

    print("\nSAMPLE CLEANED ROWS")
    print(df[cleaned_columns].sample(10, random_state=42))


if __name__ == "__main__":
    main()