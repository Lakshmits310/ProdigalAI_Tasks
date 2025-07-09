import pandas as pd
from pathlib import Path

DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
RAW_DATA_DIR = Path("C:/Users/user/Desktop/ml_pipeline_template/ml_pipeline/data/raw")
RAW_DATA_PATH = RAW_DATA_DIR / "winequality-red.csv"

def download_data():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # ✅ Read directly from URL and parse properly
    df = pd.read_csv(DATA_URL, sep=";")

    # ✅ Save clean version locally
    df.to_csv(RAW_DATA_PATH, index=False)
    print(f"Cleaned CSV saved to: {RAW_DATA_PATH}")
    print("Preview:\n", df.head())

if __name__ == "__main__":
    download_data()
