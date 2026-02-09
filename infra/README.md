# Todo Application Infrastructure

This directory contains the infrastructure code for deploying the Todo application to Kubernetes using Docker and Helm.

## Components

### Dockerfiles
- `infra/docker/frontend/Dockerfile` - Containerizes the Next.js frontend application
- `infra/docker/backend/Dockerfile` - Containerizes the FastAPI backend application

### Kubernetes Manifests
- `infra/k8s/deployments/` - Deployment configurations for frontend and backend
- `infra/k8s/services/` - Service definitions for internal networking
- `infra/k8s/ingress/` - Ingress configuration for external access
- `infra/k8s/secrets/` - Secret definitions for sensitive data
- `infra/k8s/configmaps/` - ConfigMap definitions for non-sensitive configuration

### Helm Chart
- `infra/helm/todo-app-chart/` - Complete Helm chart for easy deployment
- Contains all templates and configurations needed to deploy the application

## Deployment Instructions

### Prerequisites
- Docker
- Minikube
- Helm
- kubectl

### Steps

1. Start Minikube:
   ```bash
   minikube start
   ```

2. Build Docker images:
   ```bash
   # Build frontend image
   docker build -f infra/docker/frontend/Dockerfile -t todo-frontend:latest .
   
   # Build backend image
   docker build -f infra/docker/backend/Dockerfile -t todo-backend:latest .
   ```

3. Load images into Minikube:
   ```bash
   minikube image load todo-frontend:latest
   minikube image load todo-backend:latest
   ```

4. Create secrets (replace with actual values):
   ```bash
   kubectl create secret generic todo-app-secrets \
     --from-literal=DATABASE_URL="your-database-url" \
     --from-literal=OPENAI_API_KEY="your-openai-api-key" \
     --from-literal=AUTH_SECRET="your-auth-secret"
   ```

5. Install Helm chart:
   ```bash
   helm install todo-app-release infra/helm/todo-app-chart/ -f infra/helm/todo-app-chart/values-dev.yaml
   ```

6. Verify deployment:
   ```bash
   kubectl get pods
   kubectl get services
   kubectl get ingress
   ```

7. Access the application:
   ```bash
   minikube service todo-app-release-frontend-service
   ```

## Architecture

The infrastructure follows these principles:
- Containerization of both frontend and backend applications
- Separate deployments for frontend and backend with 2 replicas each
- Service mesh for internal communication
- Ingress for external access with path-based routing
- Secure configuration management using Kubernetes secrets and ConfigMaps
- Health checks with liveness and readiness probes
- Helm packaging for easy deployment and configuration management