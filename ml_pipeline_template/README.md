## 🧠 ML + LLM Pipeline Orchestration 🚀 
A full-cycle orchestration project that integrates a Machine Learning model pipeline with a basic Retrieval-Augmented Generation (RAG) LLM system using **Airflow**, **MLflow**, **Pandas**, **FastAPI**, and **Docker**.


## 📂 Project Structure
ml_llm_pipeline_template/
│
├── ml_pipeline/                     # Part A: ML pipeline
│   ├── dags/                        # Airflow DAGs
|   |   ├── ml_pipeline_dag.py                
│   ├── scripts/                      # Python scripts for each ML task       
|   |   ├──ingest_data.py
|   |   ├──preprocess.py
|   |   |──feature_engineering.py
|   |   ├──train_model.py
|   |   ├──evaluate_model.py
|   |   ├──log_to_mlflow.py
│   ├── model_service/                # FastAPI app for inference
|   |   ├──Dockerfile
|   |   |──main.py
|   |   ├──requirements.txt     
│   ├── data/                         # Raw, processed, and features
│   └── requirements.txt
│
├── rag_pipeline/                    # Part B: RAG pipeline
│   ├── app/                          # FastAPI + FAISS app
|   |   ├──Dockerfile
|   |   |──main.py
|   |   ├──requirements.txt 
|   |   ├──vector_store.py
│   ├── docs/                         # Input PDFs
│   ├── embeddings/                   # Vector index and chunks
│   └── requirements.txt
│
├── mlflow/                    # MLflow logs and model artifacts
│
├── docker-compose.yml         # Orchestrates all services
├── .env (optional)            # Environment variables
└── README.md                  # You're here!

## 🧪 Part A: ML Pipeline (Wine Quality Prediction)
### ⚙️ Technologies:
- Airflow (orchestration)
- Pandas (feature engineering)
- scikit-learn (model training)
- MLflow (model tracking)
- FastAPI (model serving)
- Docker (containerization)

### 🔁 Workflow:
1. **Ingest**: Load CSV (winequality-red) 
2. **Preprocess**: Clean and transform the data
3. **Feature Engineering**: Generate new features
4. **Train**: Build a classifier using scikit-learn
5. **Evaluate**: Save metrics
6. **Log**: Register model in MLflow
7. **Serve**: Deploy model via FastAPI
8. **Orchestrate**: All steps run through Airflow

### 🛠 Setup Instructions
# 1. Clone this repository or unzip the folder
git clone <your-repo-url>
cd ml_llm_pipeline_template

# 2. Start all services
docker-compose up --build


## 🔍 Testing Part A Model API
curl -X POST http://localhost:8000/predict \
-H "Content-Type: application/json" \
-d '{"data": [[7.4, 0.7, 0.0, 1.9, 0.076, 11, 34, 0.9978, 3.51, 0.56, 9.4]]}'

You’ll get:
{"predictions": [5]}


## 🧠 Part B: RAG LLM Pipeline (Mini POC)
### ⚙️ Technologies:
* FAISS (vector store)
* DistilBERT or similar model (via Hugging Face Transformers)
* PDF Ingestion + Chunking
* FastAPI (query handling)
* Docker

### 🔁 Workflow:
1. Upload PDFs (`docs/`)
2. Split and embed documents → FAISS index
3. Accept query via REST
4. Retrieve top relevant chunks
5. Use LLM to answer based on context

### 🔍 Sample RAG API Query
curl -X GET "http://localhost:8001/query?q=What is the project about?"

Response:
{
  "query": "What is the project about?",
  "answer": "This project demonstrates a full-cycle ML pipeline and a simple LLM-based RAG system..."
}


## 🎯 Airflow DAG
View and run DAGs from the Airflow UI:
* DAG ID: `wine_quality_pipeline`
* Weekly schedule (`@weekly`)
* Trigger manually or enable auto-retrain


## 📦 MLflow Artifacts
Track experiments at: `http://localhost:5000`
* Registered models
* Metrics
* Parameters
* Artifacts (model.pkl, conda.yaml, etc.)


## 🛠️ How to Rebuild and Run the ML Pipeline Project from Scratch

If you are setting up the project fresh using this template, follow the steps below:
### 📁 1. Extract the Project
unzip ml_pipeline_template.zip
cd ml_pipeline_template

### 🧼 2. (Optional) Clean Up Previous Docker Artifacts
docker system prune -af --volumes

### 📦 3. Build All Docker Images
docker-compose build --no-cache

If you face Docker Hub pull limits, run:
docker login

### 🚀 4. Start All Containers
docker-compose up -d

This will spin up the following services:

| Service         | Purpose                      | Port                         |
| --------------- | ---------------------------- | ---------------------------- |
| `airflow`       | Workflow orchestrator        | `http://localhost:8080`      |
| `mlflow`        | ML experiment tracking       | `http://localhost:5000`      |
| `model_service` | FastAPI for model serving    | `http://localhost:8000/docs` |
| `rag_service`   | FastAPI for RAG pipeline     | `http://localhost:8001/docs` |
| `spark`         | Spark job for data ingestion | —                            |
| `postgres`      | Airflow backend DB           | —                            |

### 🥪 5. Re-register the ML Model
Since model artifacts are stored in Docker volumes, you must **retrain and register the model**:
docker-compose exec airflow python /scripts/train_model.py

✅ This will:
* Train a model
* Register it as `sklearn-model` in MLflow
* Save artifacts in `/mlflow`

### 🔁 6. Restart Model Service
docker-compose restart model_service

### 📡 7. Test the Model API
Check if it works:
curl http://localhost:8000/docs

Or run a prediction:
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[7.4, 0.7, 0, 1.9, 0.076, 11, 34, 0.9978, 3.51, 0.56, 9.4]]}'

### 🧠 8. If Spark/Airflow Fails (Optional Debug)
Let Spark/Airflow start, and verify:
* Python + PySpark are installed
* Volume paths are correctly mounted
* Scripts are reachable (`/scripts/ingest_data.py`, etc.)

### ✅ Done!
You're now running the complete ML pipeline again from scratch. 🎉


