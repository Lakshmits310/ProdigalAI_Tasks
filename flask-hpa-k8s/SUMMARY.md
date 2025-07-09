# Kubernetes Horizontal Pod Autoscaler (HPA) – Summary
## 📌 Objective
Implement and demonstrate Kubernetes-based autoscaling using *Horizontal Pod Autoscaler (HPA)* on a *CPU-intensive FastAPI app, deployed via **Minikube. The goal is to autoscale pods between **1 to 10 replicas* based on *CPU utilization*.


## 🏗 Architectural Decisions
### 1. *FastAPI as the Base App*
- Chosen for lightweight and fast response.
- One endpoint (/load) was built to simulate high CPU load using Python list comprehensions and time.

### 2. *Containerization with Docker*
- The FastAPI app was containerized using a custom Dockerfile exposing port 8000.
- Base image: python:3.9-slim for small image size.

### 3. *Kubernetes Deployment (Minikube)*
- Used deployment.yaml to deploy the app with:
  - CPU requests: 100m
  - CPU limits: 500m
- A service.yaml exposed the app via NodePort.

### 4. *Horizontal Pod Autoscaler*
- Configured in hpa.yaml:
  - minReplicas: 1
  - maxReplicas: 10
  - targetCPUUtilizationPercentage: 50
- Autoscaling triggered via metrics-server.


## ⚠ Challenges Faced
| Area             | Challenge                             | Resolution                                            |
|------------------|---------------------------------------|-------------------------------------------------------|
| Metrics          |kubectl top pods returned nothing      | Installed metrics-server on Minikube manually         |
|                  |initially initially.                   |                                                       |
| Delay            |HPA didn't respond immediately to load.| Waited 30–60s after traffic started                   |
| CPU Load         |Simulated load was insufficient at     | Rewrote the load logic to use nested loops and long   |
|                  |first.                                 | iterations                                            |
| Port Access      | FastAPI not exposed properly          | Switched to NodePort and confirmed correct port in    |
|                  |minikube service list                  |                                                       |
| Scaling Down     | Pods took longer to scale down        | Waited ~5 minutes post load removal                   |


## 🧠 Scope for Improvement
### 1. *Memory-Based Autoscaling*
- Add memory-based thresholds alongside CPU in HPA.

### 2. *Visual Monitoring Tools*
- Integrate tools like:
  - Kubernetes Dashboard
  - Prometheus + Grafana

### 3. *Use of Ingress*
- Replace NodePort with Ingress + nginx for clean external access and domain routing.

### 4. *Custom Metrics*
- Implement custom metrics (e.g., request count or latency) using Prometheus Adapter for fine-grained scaling logic.

### 5. *Production-Grade Enhancements*
- Add readiness/liveness probes.
- Use rolling updates for deployment.
- Deploy on a managed cloud K8s like EKS/GKE for scalability and resilience testing.

## 🏁 Conclusion
This project successfully demonstrates autoscaling in Kubernetes using HPA with real-time traffic. It provides a strong foundation for production-level scaling solutions that can be enhanced with custom metrics, memory usage, and more intelligent orchestration.