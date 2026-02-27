# Complete CI/CD Pipeline with Jenkins 

A complete end-to-end CI/CD pipeline demonstrating automated build, test, containerization, and deployment of a Flask web application using Jenkins, Docker, and AWS EC2.

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-Jenkins-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![Python](https://img.shields.io/badge/Python-3.9-3776AB)
![Flask](https://img.shields.io/badge/Flask-3.0-000000)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Local Development](#local-development)
- [Jenkins Setup](#jenkins-setup)
- [Pipeline Stages](#pipeline-stages)
- [Deployment](#deployment)

##  Overview

This project implements a production-ready CI/CD pipeline that:

- ✅ Builds a Flask web application
- ✅ Runs comprehensive unit tests with coverage reporting
- ✅ Creates optimized Docker containers
- ✅ Pushes images to Docker Hub
- ✅ Deploys to AWS EC2 automatically
- ✅ Cleans up resources post-deployment

##  Architecture

```
GitHub → Jenkins → Docker Build → Docker Hub → EC2 Deployment
   ↓         ↓           ↓             ↓            ↓
 Webhook   Tests     Multi-stage    Registry    Auto-deploy
           pytest     Dockerfile      Push       Container
```

### Pipeline Flow

1. **Checkout**: Clone repository from GitHub
2. **Install/Build**: Install Python dependencies
3. **Test**: Run pytest with coverage reporting
4. **Docker Build**: Build optimized container image
5. **Push Image**: Push to Docker Hub registry
6. **Deploy**: SSH to EC2 and deploy container

##  Prerequisites

### Required Software

- **Jenkins LTS** (2.400+)
- **Docker** (20.10+)
- **Python** (3.9+)
- **Git**

### AWS Requirements

- **EC2 Instance** ( Ubuntu)
- **Security Group** allowing:
  - SSH (port 22)
  - HTTP (port 5000)
  - HTTPS (port 443)

### Accounts Needed

- **GitHub Account** (for repository)
- **Docker Hub Account** (for registry)
- **AWS Account** (for EC2)

## Project Structure

```
Complete_CICD_Pipeline/
├── app.py                  # Flask application
├── test_app.py            # Unit tests
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container definition
├── .dockerignore          # Docker build exclusions
├── Jenkinsfile            # Pipeline 
├── README.md             # This file
├── RUNBOOK.md            # Operational guide
└── .gitignore            # Git exclusions
```

##  Local Development

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Complete_CICD_Pipeline.git
cd Complete_CICD_Pipeline
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Application

```bash
python app.py
```

Visit: `http://localhost:5000`

### 4. Run Tests

```bash
# Run tests
pytest test_app.py -v

# Run with coverage
pytest test_app.py -v --cov=app --cov-report=html
```

### 5. Build Docker Image

```bash
# Build image
docker build -t cicd-demo-app:test .

# Run container
docker run -p 5000:5000 cicd-demo-app:test

```

## 🔧 Jenkins Setup

### Step 1: Install Required Plugins

Navigate to **Manage Jenkins** → **Manage Plugins** → **Available** and install:

- ✅ Pipeline
- ✅ Git
- ✅ Credentials Binding
- ✅ Docker Pipeline
- ✅ SSH Agent
- ✅ HTML Publisher

### Step 2: Configure Credentials

Go to **Manage Jenkins** → **Manage Credentials** → **Global** → **Add Credentials**

#### Configure Pipeline:

- **General**:
  - ✅ GitHub project: `https://github.com/YOUR_USERNAME/Complete_CICD_Pipeline`
- **Build Triggers**:
  - ✅ GitHub hook trigger for GITScm polling
- **Pipeline**:
  - **Definition**: Pipeline script from SCM
  - **SCM**: Git
  - **Repository URL**: `https://github.com/YOUR_USERNAME/Complete_CICD_Pipeline.git`
  - **Credentials**: `git_credentials` (if private)
  - **Branch**: `*/main` 
  - **Script Path**: `Jenkinsfile`

##  Pipeline Stages

### Stage 1: Checkout

Clones repository from GitHub

### Stage 2: Install Dependencies

Installs Python packages from `requirements.txt`

### Stage 3: Run Tests

Executes pytest with coverage reporting

### Stage 4: Build Docker Image

Creates multi-stage optimized Docker image

### Stage 5: Push to Registry

Pushes image to Docker Hub

### Stage 6: Deploy to EC2

- Copies deployment script to EC2
- Pulls latest image
- Stops old container
- Starts new container

### Stage 7: Verify Deployment

Tests application health endpoint

### Stage 8: Cleanup

Removes local Docker images

##  Deployment

### Automatic Trigger (GitHub Webhook)

1. Go to GitHub repository settings
2. Navigate to **Webhooks** → **Add webhook**
3. Payload URL: `http://YOUR_JENKINS_URL/github-webhook/`
4. Content type: `application/json`
5. Events: **Just the push event**

### Check Docker Container on EC2

```bash
ssh ec2-user@YOUR_EC2_IP
docker ps
docker logs cicd-demo-app
```

### Verify Cleanup

```bash
# Check Docker images
docker images

# Check stopped containers
docker ps -a
```

##  Screenshots

### Successful Pipeline Run

<img width="1918" height="969" alt="image" src="https://github.com/user-attachments/assets/d37716b1-3031-4421-8dfd-13ddad0cc4c5" />


### Application Running


<img width="1918" height="798" alt="image" src="https://github.com/user-attachments/assets/304194fa-97d4-4406-991f-56561465b364" />


### Docker Hub Image


<img width="1918" height="778" alt="image" src="https://github.com/user-attachments/assets/a6cdd139-fcc0-455b-98f8-68575f2fb79a" />










