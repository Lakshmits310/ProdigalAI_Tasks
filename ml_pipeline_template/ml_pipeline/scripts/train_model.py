import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import mlflow
import mlflow.sklearn
import os

TRAIN_PATH = "/data/features/train.parquet"
TEST_PATH = "/data/features/test.parquet"

def train_model():
    # Load the data
    train_df = pd.read_parquet(TRAIN_PATH)
    test_df = pd.read_parquet(TEST_PATH)

    X_train = train_df.drop("quality", axis=1)
    y_train = train_df["quality"]
    X_test = test_df.drop("quality", axis=1)
    y_test = test_df["quality"]

    # Set MLflow tracking URI
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))

    # Set MLflow artifact path
    os.environ["MLFLOW_ARTIFACT_URI"] = os.getenv("MLFLOW_ARTIFACT_URI", "/mlflow")

    with mlflow.start_run():
        model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        rmse = mean_squared_error(y_test, predictions, squared=False)

        mlflow.log_metric("rmse", rmse)

        # ✅ REGISTER the model properly here:
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="sklearn-model"  # 🔥 Required
        )

        print(f"✅ Model trained and registered as 'sklearn-model' with RMSE: {rmse:.4f}")

if __name__ == "__main__":
    train_model()
