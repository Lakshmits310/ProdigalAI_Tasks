import pandas as pd
from pathlib import Path

RAW_DATA_PATH = "/data/raw/winequality-red.csv"
PROCESSED_DATA_PATH = "/data/processed/wine_processed.parquet"

def preprocess_data():
    df = pd.read_csv(RAW_DATA_PATH)  # ⬅️ Removed `sep=";"` since it's actually comma-separated
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    Path("/data/processed").mkdir(parents=True, exist_ok=True)
    df.to_parquet(PROCESSED_DATA_PATH, index=False)
    print(f"✅ Processed data saved to: {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    preprocess_data()
