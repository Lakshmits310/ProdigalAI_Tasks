## 📌 Project Title
*High-Throughput API Ingestion with Kafka, Zookeeper, Docker, and Scalable Consumers*

## ✅ Objective
To simulate high-volume API ingestion (10,000+ requests/min) using Kafka for event queuing and scalable consumers for processing, ensuring durability, reliability, and delivery guarantees.


## ⚙ Key Components
- *Kafka + Zookeeper* via Docker Compose for messaging and coordination.
- *Flask APIs*:
  - /register_event: Receives and pushes messages to Kafka.
  - /get_status: Returns system status / health checks.
- *Kafka Producer* integrated in Flask.
- *Kafka Consumer* to process and log/store incoming messages.
- *Load Generator* to simulate 10,000+ API requests per minute.
- *Error Handling & Retry Logic* in consumers.
- *Kafka Topology Diagram* for architectural clarity.


## 🧠 Architectural Decisions
1. *Kafka for Event Streaming*:  
   Kafka was chosen to handle high-throughput ingestion due to its scalability, durability, and message persistence guarantees.

2. *Docker Compose*:  
   Simplified local setup of Kafka, Zookeeper, and the API services, providing an isolated and reproducible environment.

3. *Flask Framework*:  
   A lightweight framework sufficient for the dummy APIs, quick to implement and easy to deploy.

4. *Multithreaded Load Simulation*:  
   Used Python's threading module to send concurrent requests and stress-test the system effectively.

5. *Consumer Scalability*:  
   Designed the consumer logic to be horizontally scalable by using Kafka's partition-based message distribution.

6. *Offset Management & Retry*:  
   Set auto_offset_reset=earliest to allow replay, and managed retries within consumer logic for fault tolerance.


## ⚠ Challenges Faced
1. *Kafka Client Compatibility Issues*:  
   Initial issues with kafka-python versions and Docker Kafka port mappings delayed local testing.

2. *Handling Consumer Failures Gracefully*:  
   Ensuring retry without infinite loops or message duplication required extra care in try-except blocks and offset handling.

3. *Simulating Real Load*:  
   Python threading helped, but hitting 10K+ req/min without overwhelming the local machine needed rate limiting and batching tweaks.

4. *API Bottleneck under Load*:  
   Flask, being single-threaded by default, struggled under high concurrency. A WSGI server like Gunicorn was considered.

5. *Durability Proof*:  
   Demonstrating message persistence under container restarts required configuration of Kafka volumes and replay testing.


## 📈 Scope for Improvement
1. *Use of Kafka Partitions*:  
   Currently, all messages go to a single partition. Partitioning based on user ID or event type would enable true consumer parallelism.

2. *Deploy on Kubernetes*:  
   Container orchestration via Kubernetes can help with horizontal scaling of producers and consumers.

3. *Use of Gunicorn/Uvicorn*:  
   Deploying the Flask app using Gunicorn (or Uvicorn for FastAPI) can better handle concurrent requests.

4. *Persist Processed Events to DB*:  
   Instead of logging to console, storing processed messages in a database (PostgreSQL, MongoDB, etc.) would make it more production-ready.

5. *Implement Dead Letter Queue*:  
   Messages that repeatedly fail processing can be routed to a DLQ for further inspection instead of retrying infinitely.

6. *Cloud Integration (Bonus)*:  
   Deploying the ingestion API via AWS Lambda + API Gateway and using Amazon MSK (Managed Kafka) would make this system cloud-native.
