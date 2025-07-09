from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.sklearn
import pandas as pd
import os

app = FastAPI()

MODEL_URI = "models:/sklearn-model/latest"

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))

try:
    model = mlflow.sklearn.load_model(MODEL_URI)
except Exception as e:
    raise RuntimeError(f"❌ Could not load model from {MODEL_URI}: {e}")

# ✅ Add health check route
@app.get("/health")
def health():
    return {"status": "model service up", "model_loaded": model is not None}


class InputData(BaseModel):
    data: list  # List of feature lists

@app.post("/predict")
def predict(input_data: InputData):
    try:
        df = pd.DataFrame(input_data.data)
        predictions = model.predict(df).tolist()
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    print("✅ Loaded model type:", type(model))

# ✅ Add this to actually start the server (if not already present)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

