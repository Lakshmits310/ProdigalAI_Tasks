# 🚀 Kubernetes Pod Autoscaling with Flask + HPA
## 📌 Objective
To implement a **scalable Kubernetes deployment** using **Horizontal Pod Autoscaler (HPA)** that adjusts the number of pods based on CPU usage of a **Flask-based dummy web application**.


## 📁 Folder Structure
flask-hpa-k8s/
│
├── app.py                  # Flask app with a CPU load endpoint
├── requirements.txt        # Flask dependencies
├── Dockerfile              # For building container image
├── load_generator.py       # Script to simulate heavy CPU load
│
├── k8s/                    # Kubernetes configuration files
│   ├── deployment.yaml     # K8s Deployment for Flask app
│   ├── service.yaml        # K8s Service (NodePort)
│   └── hpa.yaml            # Horizontal Pod Autoscaler config
│
└── README.md               # Project guide and documentation


## 🛠️ Technologies Used
- Python 3, Flask
- Docker
- Kubernetes (Minikube)
- Horizontal Pod Autoscaler (HPA)
- Metrics Server (enabled in Minikube)


## 🚀 Step-by-Step Implementation
### 🔧 1. Build Docker Image
Open terminal in the root folder (`flask-hpa-k8s/`):
docker build -t flask-hpa-app .
> Builds the image using Dockerfile.

### 🐳 2. Load Docker Image into Minikube
minikube image load flask-hpa-app
> Loads the local Docker image into Minikube's internal registry.

### 📦 3. Apply Kubernetes Deployment and Service
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
> Deploys the Flask app and exposes it via NodePort.

### 🌐 4. Get the Service URL
minikube service flask-service --url
> Use the URL to access Flask app in browser or script (e.g., `http://127.0.0.1:PORT`)

### 📈 5. Apply Horizontal Pod Autoscaler
kubectl apply -f k8s/hpa.yaml
> Configures HPA to monitor CPU and scale pods between 1–10.

### 🔁 6. Trigger Load (Simulate Traffic)
python load_generator.py
> This sends multiple requests to `/load` endpoint to simulate CPU stress.

### 📊 7. Monitor HPA Activity and Pod Scaling
kubectl get hpa -w
> You will see CPU usage rise and replicas increase (e.g., from 1 to 5+ pods).

kubectl get pods -w
> Shows pods being created and started as autoscaler scales up.

## 🔍 What to Expect (Expected Output)
* The app initially runs with **1 pod**
* When CPU > 50%, HPA scales up to more pods (up to 10)
* After traffic ends and CPU drops, HPA scales pods back down

## 🌐 Access the App
* `http://<minikube-ip>:<node-port>/` → should show `Hello from Flask!`
* `http://<minikube-ip>:<node-port>/load` → simulates 10s of CPU stress

## 🧪 Testing with Curl (Optional)
curl http://localhost:<node-port>/
curl http://localhost:<node-port>/load
