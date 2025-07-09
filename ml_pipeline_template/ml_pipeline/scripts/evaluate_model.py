import pandas as pd
import mlflow
import mlflow.sklearn
import os
from sklearn.metrics import mean_squared_error

TEST_PATH = "/data/features/test.parquet"
MODEL_URI = "models:/WineQuality/Production"

def evaluate_model():
    # Set MLflow tracking URI
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
    
    # Load test data using pandas
    test_df = pd.read_parquet(TEST_PATH)

    # Split into features and target
    X_test = test_df.drop(columns=["quality"])
    y_test = test_df["quality"]
    
    # Load model from MLflow Model Registry
    model = mlflow.sklearn.load_model(MODEL_URI)
    
    # Predict
    predictions = model.predict(X_test)
    
    # Calculate RMSE
    rmse = mean_squared_error(y_test, predictions, squared=False)
    print(f"Model RMSE: {rmse}")
    
    # Log metrics to MLflow
    with mlflow.start_run():
        mlflow.log_metric("test_rmse", rmse)
        mlflow.log_param("eval_dataset", "test_split")

if __name__ == "__main__":
    evaluate_model()
