# Quickstart Guide: Infrastructure Deployment (Docker, Kubernetes, Helm)

## Overview
This guide provides step-by-step instructions to deploy the Todo application using Docker, Kubernetes (Minikube), and Helm.

## Prerequisites
- Docker installed and running
- Minikube installed and running
- kubectl installed
- Helm installed
- Access to the existing Todo application codebase (frontend and backend)

## Step-by-Step Instructions

### 1. Start Minikube
```bash
minikube start
```

### 2. Build Docker Images
```bash
# Navigate to the project root
cd /path/to/todo-app

# Build frontend image
docker build -t todo-frontend:latest ./apps/frontend

# Build backend image
docker build -t todo-backend:latest ./apps/backend
```

### 3. Load Images into Minikube
```bash
# Load frontend image
minikube image load todo-frontend:latest

# Load backend image
minikube image load todo-backend:latest
```

### 4. Create Kubernetes Secrets
```bash
kubectl create secret generic todo-app-secrets \
  --from-literal=DATABASE_URL=<your-database-url> \
  --from-literal=OPENAI_API_KEY=<your-openai-api-key> \
  --from-literal=AUTH_SECRET=<your-auth-secret>
```

### 5. Install Helm Chart
```bash
# Navigate to the Helm chart directory
cd ./infra/helm/todo-app-chart

# Install the chart
helm install todo-app-release . -f values-dev.yaml
```

### 6. Verify Deployment
```bash
# Check if pods are running
kubectl get pods

# Check services
kubectl get services

# Check ingress
kubectl get ingress
```

### 7. Access the Application
```bash
# Get the Minikube IP
minikube ip

# Access the frontend at http://<minikube-ip>
# Access the backend API at http://<minikube-ip>/api
```

## Troubleshooting Common Issues
- If pods are not starting, check logs with `kubectl logs <pod-name>`
- If ingress is not working, verify the ingress controller is running
- If services are not accessible, check firewall settings
- If secrets are not mounting, verify they were created correctly

## Next Steps
- Configure SSL certificates for HTTPS
- Set up monitoring and logging
- Implement CI/CD pipeline for automated deployments