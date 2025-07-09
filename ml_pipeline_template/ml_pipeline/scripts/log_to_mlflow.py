import mlflow
import os
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession

MODEL_PATH = "/data/models/spark-model"
MODEL_NAME = "WineQuality"

def log_model():
    spark = SparkSession.builder \
        .appName("MLflowLogger") \
        .getOrCreate()
    
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
    
    model = PipelineModel.load(MODEL_PATH)
    
    with mlflow.start_run():
        mlflow.spark.log_model(
            model,
            "spark-model",
            registered_model_name=MODEL_NAME
        )
        mlflow.log_param("model_type", "RandomForestRegressor")
        print(f"Model logged to MLflow as '{MODEL_NAME}'")

if __name__ == "__main__":
    log_model()