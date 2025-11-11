# Kubernetes Orchestration - Django Messaging App

## Overview
This directory contains Kubernetes configuration files and scripts for deploying, scaling, and managing the Django messaging app using Kubernetes orchestration.

## Prerequisites

### Required Tools
- **Minikube**: Local Kubernetes cluster
- **kubectl**: Kubernetes command-line tool
- **Docker**: Container runtime
- **curl**: For testing endpoints
- **wrk** (optional): Load testing tool

### Installation Commands

**macOS:**
```bash
# Install Minikube
brew install minikube

# Install kubectl
brew install kubectl

# Install wrk (optional)
brew install wrk
```

**Linux:**
```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install wrk
sudo apt-get install wrk
```

## Project Structure

```
messaging_app/
├── kurbeScript                 # Task 0: Start and verify Kubernetes cluster
├── deployment.yaml            # Task 1: Django app deployment with ClusterIP service
├── kubctl-0x01               # Task 2: Scale deployment and perform load testing
├── ingress.yaml              # Task 3: Ingress configuration for external access
├── commands.txt              # Task 3: Ingress setup commands
├── blue_deployment.yaml      # Task 4 & 5: Blue version deployment (v2.0)
├── green_deployment.yaml     # Task 4: Green version deployment (v1.1)
├── kubeservice.yaml          # Task 4: Services for blue-green deployment
├── kubctl-0x02              # Task 4: Blue-green deployment script
├── kubctl-0x03              # Task 5: Rolling update with zero-downtime testing
└── KUBERNETES_README.md     # This file
```

## Tasks Implementation

### Task 0: Install Kubernetes and Set Up Local Cluster

**File**: `kurbeScript`

**Purpose**: Initialize Minikube cluster and verify setup

**Usage**:
```bash
./kurbeScript
```

**What it does**:
- Checks if Minikube is installed
- Starts Minikube cluster
- Verifies cluster with `kubectl cluster-info`
- Lists all pods and nodes

---

### Task 1: Deploy Django Messaging App

**File**: `deployment.yaml`

**Purpose**: Deploy Django app with ClusterIP service

**Features**:
- Single replica deployment
- Container image: `messaging-app:1.0`
- Environment variables for database configuration
- Liveness and readiness probes
- Resource limits (256Mi-512Mi memory, 250m-500m CPU)
- ClusterIP service on port 80

**Usage**:
```bash
# Apply deployment
kubectl apply -f deployment.yaml

# Check pods
kubectl get pods

# Check logs
kubectl logs <pod-name>

# Check service
kubectl get svc django-service
```

---

### Task 2: Scale Django App

**File**: `kubctl-0x01`

**Purpose**: Scale app to 3 replicas and perform load testing

**What it does**:
- Scales deployment to 3 replicas
- Waits for pods to be ready
- Monitors resource usage with `kubectl top`
- Performs load testing with `wrk` (if available)

**Usage**:
```bash
./kubctl-0x01
```

**Manual scaling**:
```bash
kubectl scale deployment django-messaging-app --replicas=3
kubectl get pods -w
```

---

### Task 3: Set Up Kubernetes Ingress

**Files**: `ingress.yaml`, `commands.txt`

**Purpose**: Expose Django app externally using Nginx Ingress

**Features**:
- Nginx Ingress controller
- Routes for `/`, `/api/`, `/admin/`
- Host-based routing: `messaging.local`
- SSL redirect disabled (for local development)

**Setup**:
```bash
# Enable ingress addon
minikube addons enable ingress

# Apply ingress configuration
kubectl apply -f ingress.yaml

# Get Minikube IP
minikube ip

# Add to /etc/hosts
echo "$(minikube ip) messaging.local" | sudo tee -a /etc/hosts

# Test
curl http://messaging.local/
curl http://messaging.local/api/
curl http://messaging.local/admin/
```

---

### Task 4: Blue-Green Deployment Strategy

**Files**: `blue_deployment.yaml`, `green_deployment.yaml`, `kubeservice.yaml`, `kubctl-0x02`

**Purpose**: Implement zero-downtime deployment with blue-green strategy

**Versions**:
- **Blue**: `messaging-app:1.0` (initial version)
- **Green**: `messaging-app:1.1` (new version)

**Services**:
- `django-service`: Main service (routes to blue or green)
- `django-service-blue`: Direct access to blue version
- `django-service-green`: Direct access to green version

**Usage**:
```bash
# Deploy both versions
./kubctl-0x02

# Switch traffic to green
kubectl patch service django-service -p '{"spec":{"selector":{"version":"green"}}}'

# Switch back to blue
kubectl patch service django-service -p '{"spec":{"selector":{"version":"blue"}}}'

# Verify
kubectl get svc django-service -o yaml | grep version
```

---

### Task 5: Rolling Updates

**Files**: `blue_deployment.yaml` (updated to v2.0), `kubctl-0x03`

**Purpose**: Update application without downtime using rolling updates

**Features**:
- Image version updated to `messaging-app:2.0`
- Rolling update strategy: `maxSurge: 1`, `maxUnavailable: 0`
- Continuous health checking during update
- Zero-downtime verification with curl requests

**Usage**:
```bash
./kubctl-0x03
```

**What it does**:
1. Shows current deployment status
2. Applies updated deployment (v2.0)
3. Monitors rollout status
4. Sends continuous requests to verify zero downtime
5. Reports success/failure statistics
6. Shows rollout history

**Manual rollback**:
```bash
kubectl rollout undo deployment/django-messaging-blue
```

---

## Building Docker Images

Before deploying to Kubernetes, build the Docker images:

```bash
# Build initial version
docker build -t messaging-app:1.0 .

# Build version 1.1 (for green deployment)
docker build -t messaging-app:1.1 .

# Build version 2.0 (for rolling update)
docker build -t messaging-app:2.0 .

# Load images into Minikube
minikube image load messaging-app:1.0
minikube image load messaging-app:1.1
minikube image load messaging-app:2.0
```

## Secrets Setup

Create required secrets for the application:

```bash
# MySQL credentials
kubectl create secret generic mysql-secret \
  --from-literal=database=messaging_app_db \
  --from-literal=username=messaging_user \
  --from-literal=password=messaging_pass123

# Django secret key
kubectl create secret generic django-secret \
  --from-literal=secret-key='django-insecure-d&ezddva!x8az*_q9c9^3)ns^k*&^!c3-^(9f*6qy(=$r=ed#9'
```

## Monitoring and Troubleshooting

### Common Commands

```bash
# Check all resources
kubectl get all

# Describe deployment
kubectl describe deployment <deployment-name>

# View logs
kubectl logs <pod-name> -f

# Get pod details
kubectl describe pod <pod-name>

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/bash

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Enable metrics server
minikube addons enable metrics-server

# View resource usage
kubectl top nodes
kubectl top pods
```

### Troubleshooting

**Pods not starting:**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Image pull errors:**
```bash
# Verify image exists in Minikube
minikube ssh docker images | grep messaging-app

# Load image if missing
minikube image load messaging-app:1.0
```

**Service not accessible:**
```bash
# Get service URL
minikube service <service-name> --url

# Port forward for testing
kubectl port-forward service/<service-name> 8080:80
```

## Best Practices Implemented

✅ **Declarative Configuration**: All resources defined in YAML files
✅ **Health Checks**: Liveness and readiness probes configured
✅ **Resource Limits**: CPU and memory requests/limits defined
✅ **Labels and Selectors**: Proper labeling for organization
✅ **Rolling Updates**: Zero-downtime deployment strategy
✅ **Blue-Green Deployment**: Quick rollback capability
✅ **Secrets Management**: Sensitive data in Kubernetes secrets
✅ **Service Isolation**: ClusterIP for internal services
✅ **Ingress Controller**: External access management

## Important Notes

⚠️ **Kubernetes Not Installed**: This machine does not have Kubernetes/Minikube installed. All files are prepared and ready for deployment when Kubernetes is available.

⚠️ **Docker Images**: The Docker images (`messaging-app:1.0`, `1.1`, `2.0`) need to be built from the Dockerfile before deployment.

⚠️ **Secrets**: Create the MySQL and Django secrets before applying deployments.

⚠️ **Local Development**: All configurations are optimized for local Minikube development. Production deployments require additional hardening.

## Repository Information

- **Repository**: alx-backend-python
- **Directory**: messaging_app
- **Assessment**: Manual peer review required

## Quick Start Guide

When Kubernetes is available:

```bash
# 1. Start cluster
./kurbeScript

# 2. Create secrets
kubectl create secret generic mysql-secret --from-literal=database=messaging_app_db --from-literal=username=messaging_user --from-literal=password=messaging_pass123
kubectl create secret generic django-secret --from-literal=secret-key='your-secret-key'

# 3. Build and load Docker images
docker build -t messaging-app:1.0 .
minikube image load messaging-app:1.0

# 4. Deploy application
kubectl apply -f deployment.yaml

# 5. Verify deployment
kubectl get pods
kubectl get svc

# 6. Scale application
./kubctl-0x01

# 7. Setup ingress
minikube addons enable ingress
kubectl apply -f ingress.yaml

# 8. Test blue-green deployment
./kubctl-0x02

# 9. Perform rolling update
./kubctl-0x03
```

## Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Blue-Green Deployments](https://kubernetes.io/blog/2018/04/30/zero-downtime-deployment-kubernetes-jenkins/)
- [Rolling Updates](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)

---

**Ready for Kubernetes deployment!** 🚀
