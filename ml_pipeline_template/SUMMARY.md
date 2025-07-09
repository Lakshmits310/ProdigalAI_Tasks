## 🔍 Project Overview
This project demonstrates a full-cycle orchestration of an ML pipeline and a Retrieval-Augmented Generation (RAG) system using:

- *Airflow* for pipeline orchestration
- *Pandas* for preprocessing and feature engineering (PySpark planned but skipped)
- *scikit-learn* for ML model training
- *MLflow* for experiment tracking and model versioning
- *FastAPI* for serving both ML and LLM APIs
- *FAISS* and *DistilBERT* for document retrieval
- *Docker Compose* for container orchestration

The goal was to simulate real-world machine learning operations (MLOps) and intelligent information retrieval with a minimal but scalable architecture.


## ⚙ Architectural Decisions
### 1. Modular ML Pipeline
Each pipeline task (ingestion, preprocessing, training, etc.) is implemented as a separate script under ml_pipeline/scripts/. This allows independent testing and debugging.

### 2. Airflow as the Orchestrator
Airflow DAGs are used to define and execute the full ML lifecycle — from data ingestion to model logging. Tasks are sequential and built to be extendable.

### 3. MLflow for Model Tracking
MLflow is used to:
- Log hyperparameters and metrics
- Register and version models
- Track model performance visually through its web interface

### 4. FastAPI Microservices
Two separate FastAPI apps were developed:
- *ML model service*: for predicting wine quality
- *RAG service*: for querying embedded documents

### 5. FAISS + DistilBERT for Retrieval
Documents are ingested from PDFs, chunked into passages, and embedded using SentenceTransformers (DistilBERT). The embeddings are indexed in FAISS for fast retrieval based on user queries.

### 6. Docker Compose Integration
All components are containerized:
- Airflow (scheduler, webserver)
- MLflow server
- FastAPI services for ML and RAG
This ensures reproducibility and a production-like local environment.


## 🚧 Challenges Faced
### 🔄 Airflow Integration
- Configuring DAGs with external Python scripts required adjusting imports and file paths.
- Volume sharing and environment consistency across Docker containers took careful setup.

### ⚠ MLflow Tracking
- Tracking models from within Airflow tasks required setting up correct experiment contexts and manual logging in some cases.

### 🔥 PySpark Installation Issue
- Initially intended to use PySpark for data ingestion and preprocessing in a distributed fashion.
- Encountered persistent installation and compatibility issues with pyspark in the Docker environment.
- As a workaround, used *Pandas* instead. This reduced the scalability aspect of the ingestion step, which could have benefited from Spark's parallelism.

### 🧠 FAISS and Embedding Pipeline
- Chunking documents meaningfully while preserving context was difficult.
- Indexing dynamic documents with FAISS could lead to stale or unindexed results unless managed carefully.

### 🐳 Docker Complexity
- Managing multiple exposed ports, shared volumes, and container health checks added overhead.
- Airflow’s container setup (scheduler, webserver, and DAGs) was especially sensitive to path configurations.


## 🔮 Scope for Improvement
### ✅ ML Pipeline Improvements
- Retry failed DAG tasks automatically using Airflow’s built-in features.
- Enable real-time monitoring of pipeline performance via Prometheus/Grafana.
- Add email/Slack alerts for failures.

### 🧪 Testing & CI/CD
- Add unit and integration tests for ML tasks and API endpoints.
- Set up GitHub Actions or GitLab CI for continuous integration and linting.

### 📈 MLflow Enhancements
- Automatically promote top-performing models to the “Production” stage.
- Implement rollback and version comparison via API.

### ⚙ Spark-Based Scalability
- Reintroduce PySpark by debugging installation in the container.
- Migrate data ingestion and transformation steps to Spark for handling large-scale datasets efficiently.

### 🤖 RAG Pipeline Enhancements
- Implement better chunking strategies (e.g., sentence-level + sliding windows).
- Replace DistilBERT with a lightweight generation model (TinyLLaMA or Mistral-7B via HuggingFace).
- Build a React/Vue-based UI for chat-like interactions with the RAG system.
- Add multi-document support and dynamic document uploads.


## ✅ Conclusion
This project demonstrates an end-to-end ML + LLM pipeline using a realistic orchestration stack. While PySpark integration was dropped due to technical constraints, the modular architecture allows it to be added later. The combination of Airflow, MLflow, and FastAPI with containerized deployment shows how modern ML systems can be built for repeatability, scalability, and ease of deployment.