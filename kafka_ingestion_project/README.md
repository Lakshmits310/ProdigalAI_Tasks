# Kafka High-Throughput API Ingestion
## 🧩 Objective
Simulate high-throughput event ingestion using Kafka with Flask APIs, Kafka Producer/Consumer setup, load testing, and optional AWS Lambda integration.

## 🛠️ Tech Stack
- Apache Kafka + Zookeeper (via Docker Compose)
- Flask for API endpoints
- Python Kafka Producer and Consumer (`confluent_kafka`)
- Concurrent load testing using `ThreadPoolExecutor`
- Optional AWS Lambda + API Gateway (Bonus)

## 📦 Project Structure
kafka_ingestion_project/
├── app/
│   ├── producer_app.py       # Flask app with /register_event and /get_status
│   ├── consumer_app.py       # Kafka consumer with logging and retry
│   └── templates/
│       └── index.html        # Optional HTML template
├── docker-compose.yml        # Kafka + Zookeeper services
├── load_test.py              # Simulates 10,000+ requests
├── requirements.txt          # Python dependencies
└── run_all.py                # Script to start components


## 🚀 How to Run
### Recommended: Run Everything with One Command
python run_all.py

This will:
Start the Flask API server
Start the Kafka consumer
Simulate 10,000+ requests to /register_event

⚠️ Make sure Docker containers for Kafka and Zookeeper are running before executing this script:
docker-compose up -d


### ⚙️ Manual Steps (for debugging/development)
Start Kafka + Zookeeper
docker-compose up -d

### 1. Install Python Dependencies:
pip install -r requirements.txt

### 2. Run Flask API
python app/producer_app.py

### 3. Run Kafka Consumer
python app/consumer_app.py

### 4. Run Load Test
python load_test.py


## 🌐 API Endpoints
Endpoint          |	Method       |	Description              |
------------------|--------------|---------------------------|
/register_event   |	POST         |	Sends an event to Kafka  |
/get_status       |	GET	         | Health check              |

## 📈 Kafka Topology
[Load Test] → [Flask API /register_event] → [Kafka Topic: events] → [Kafka Consumer(s)]

## ✅ Features
-Structured Logging
-Error Handling with Retry
-Threaded High-Load Simulation
-Single Command Setup via run_all.py

## 🧪 Future Improvements
-Dockerize Flask API and Consumer
-Add Kafka REST Proxy
-Support JSON schema validation
-Use Prometheus/Grafana for metrics

