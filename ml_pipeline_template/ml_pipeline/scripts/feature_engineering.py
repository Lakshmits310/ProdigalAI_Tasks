import pandas as pd
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import numpy as np

PROCESSED_DATA_PATH = "/data/processed/wine_processed.parquet"
FEATURES_DIR = "/data/features"
TRAIN_PATH = f"{FEATURES_DIR}/train.parquet"
TEST_PATH = f"{FEATURES_DIR}/test.parquet"

def feature_engineering():
    # Load processed data
    df = pd.read_parquet(PROCESSED_DATA_PATH)

    # Feature columns (excluding target)
    feature_cols = [col for col in df.columns if col != 'quality']

    # Split features and target
    X = df[feature_cols]
    y = df["quality"]

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Combine scaled features and target
    df_scaled = pd.DataFrame(X_scaled, columns=feature_cols)
    df_scaled["quality"] = y.values

    # Split into train and test sets
    train_df = df_scaled.sample(frac=0.8, random_state=42)
    test_df = df_scaled.drop(train_df.index)

    # Ensure output directories exist
    Path(FEATURES_DIR).mkdir(parents=True, exist_ok=True)

    # Save to Parquet
    train_df.to_parquet(TRAIN_PATH, index=False)
    test_df.to_parquet(TEST_PATH, index=False)

    print(f"Train and test features saved to {FEATURES_DIR}")

if __name__ == "__main__":
    feature_engineering()
