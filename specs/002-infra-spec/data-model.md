# Data Model: Infrastructure Deployment (Docker, Kubernetes, Helm)

## Overview
This document describes the data structures and configurations for the infrastructure deployment of the Todo application.

## Kubernetes Resources

### Frontend Deployment
- **Kind**: Deployment
- **Name**: todo-frontend
- **Replicas**: 2
- **Container Image**: todo-frontend:latest
- **Ports**: 3000 (exposed)
- **Environment Variables**: 
  - REACT_APP_API_URL (from ConfigMap)
- **Volume Mounts**: None
- **Liveness Probe**: None (frontend is stateless)
- **Readiness Probe**: None (frontend is stateless)

### Backend Deployment
- **Kind**: Deployment
- **Name**: todo-backend
- **Replicas**: 2
- **Container Image**: todo-backend:latest
- **Ports**: 8000 (exposed)
- **Environment Variables**:
  - DATABASE_URL (from Secret)
  - OPENAI_API_KEY (from Secret)
  - AUTH_SECRET (from Secret)
- **Volume Mounts**: None
- **Liveness Probe**: HTTP GET /api/v1/health
- **Readiness Probe**: HTTP GET /api/v1/health

### Frontend Service
- **Kind**: Service
- **Name**: frontend-service
- **Type**: ClusterIP
- **Port**: 80
- **Target Port**: 3000
- **Selector**: app=todo-frontend

### Backend Service
- **Kind**: Service
- **Name**: backend-service
- **Type**: ClusterIP
- **Port**: 80
- **Target Port**: 8000
- **Selector**: app=todo-backend

### Ingress
- **Kind**: Ingress
- **Name**: todo-app-ingress
- **Rules**:
  - Path: /
    - Backend: frontend-service
  - Path: /api
    - Backend: backend-service

### Secrets
- **DATABASE_URL**: Encrypted database connection string
- **OPENAI_API_KEY**: Encrypted OpenAI API key
- **AUTH_SECRET**: Encrypted authentication secret

### ConfigMaps
- **API_BASE_URL**: Base URL for API connections
- **ENVIRONMENT_NAME**: Name of the deployment environment (dev, staging, prod)

## Helm Chart Structure

### Chart.yaml
- **Name**: todo-app-chart
- **Version**: 1.0.0
- **AppVersion**: 1.0.0

### Values.yaml
- **frontend.image.repository**: todo-frontend
- **frontend.image.tag**: latest
- **frontend.replicaCount**: 2
- **backend.image.repository**: todo-backend
- **backend.image.tag**: latest
- **backend.replicaCount**: 2
- **ingress.enabled**: true
- **service.type**: ClusterIP

### Templates
- **deployment.yaml**: Template for both frontend and backend deployments
- **service.yaml**: Template for both frontend and backend services
- **ingress.yaml**: Template for ingress configuration
- **secret.yaml**: Template for secrets (values provided separately)
- **configmap.yaml**: Template for configuration values