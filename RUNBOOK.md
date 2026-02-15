# CI/CD Pipeline Deployment Runbook

## 📖 Purpose

This runbook provides step-by-step instructions for deploying and operating the CI/CD pipeline.

---

## 🎯 Quick Start Checklist

- [ ] EC2 instance running with Docker installed
- [ ] Jenkins server installed and accessible
- [ ] Docker Hub account created
- [ ] GitHub repository created
- [ ] All credentials configured in Jenkins
- [ ] Security groups configured

---

## 1️⃣ EC2 Instance Setup

### Launch EC2 Instance

```bash
# Instance specifications
Type: t2.micro (or larger)
OS: Amazon Linux 2 or Ubuntu 20.04+
Storage: 20 GB
```

### Configure Security Group

| Type       | Protocol | Port | Source    |
| ---------- | -------- | ---- | --------- |
| SSH        | TCP      | 22   | Your IP   |
| Custom TCP | TCP      | 5000 | 0.0.0.0/0 |
| HTTP       | TCP      | 80   | 0.0.0.0/0 |

### Install Docker on EC2

**For Amazon Linux 2:**

```bash
# Connect to EC2
ssh -i your-key.pem ec2-user@YOUR_EC2_IP

# Update system
sudo yum update -y

# Install Docker
sudo yum install docker -y

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker ec2-user

# Logout and login again
exit
```

**For Ubuntu:**

```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Update system
sudo apt update -y

# Install Docker
sudo apt install docker.io -y

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker ubuntu

# Logout and login again
exit
```

### Verify Docker Installation

```bash
# Reconnect
ssh -i your-key.pem ec2-user@YOUR_EC2_IP

# Test Docker
docker --version
docker ps
```

---

## 2️⃣ Jenkins Server Setup

### Install Jenkins

**For Ubuntu/Debian:**

```bash
# Install Java
sudo apt update
sudo apt install openjdk-11-jdk -y

# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt update
sudo apt install jenkins -y

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Get initial password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### Install Docker on Jenkins Server

```bash
# Install Docker
sudo apt install docker.io -y

# Add Jenkins user to docker group
sudo usermod -aG docker jenkins

# Restart Jenkins
sudo systemctl restart jenkins
```

### Access Jenkins

1. Open browser: `http://JENKINS_SERVER_IP:8080`
2. Enter initial admin password
3. Install suggested plugins
4. Create admin user

---

## 3️⃣ Jenkins Configuration

### Install Required Plugins

1. Go to **Manage Jenkins** → **Manage Plugins**
2. Click **Available** tab
3. Search and install:
   - Pipeline
   - Git plugin
   - Credentials Binding Plugin
   - Docker Pipeline
   - SSH Agent Plugin
   - HTML Publisher plugin

4. Restart Jenkins: `http://JENKINS_SERVER_IP:8080/restart`

### Configure Credentials

#### Add Docker Hub Credentials

1. **Manage Jenkins** → **Manage Credentials**
2. Click **(global)** → **Add Credentials**
3. Fill in:
   - Kind: `Username with password`
   - Scope: `Global`
   - Username: `your-dockerhub-username`
   - Password: `your-dockerhub-password-or-token`
   - ID: `registry_creds`
   - Description: `Docker Hub Credentials`
4. Click **OK**

#### Add EC2 SSH Credentials

1. **Manage Jenkins** → **Manage Credentials**
2. Click **(global)** → **Add Credentials**
3. Fill in:
   - Kind: `SSH Username with private key`
   - Scope: `Global`
   - ID: `ec2_ssh`
   - Username: `ec2-user` (or `ubuntu`)
   - Private Key: Click **Enter directly**
   - Paste your EC2 private key (.pem content)
   - Description: `EC2 SSH Key`
4. Click **OK**

#### Add GitHub Credentials (Optional)

1. **Manage Jenkins** → **Manage Credentials**
2. Click **(global)** → **Add Credentials**
3. Fill in:
   - Kind: `Username with password`
   - Scope: `Global`
   - Username: `your-github-username`
   - Password: `GitHub Personal Access Token`
   - ID: `git_credentials`
   - Description: `GitHub Credentials`
4. Click **OK**

---

## 4️⃣ GitHub Repository Setup

### Create Repository

```bash
# On your local machine
cd Complete_CICD_Pipeline

# Initialize git (if not already)
git init

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/Complete_CICD_Pipeline.git

# Add all files
git add .

# Commit
git commit -m "Initial commit: Complete CI/CD Pipeline"

# Push to GitHub
git push -u origin main
```

### Configure GitHub Webhook (Optional)

1. Go to repository settings on GitHub
2. Click **Webhooks** → **Add webhook**
3. Configure:
   - Payload URL: `http://YOUR_JENKINS_IP:8080/github-webhook/`
   - Content type: `application/json`
   - Which events: `Just the push event`
   - Active: ✅
4. Click **Add webhook**

---

## 5️⃣ Update Configuration Files

### Update Jenkinsfile

Edit the `Jenkinsfile` and update these variables:

```groovy
DOCKER_IMAGE = 'YOUR_DOCKERHUB_USERNAME/cicd-demo-app'
EC2_HOST = 'YOUR_EC2_PUBLIC_IP'
EC2_USER = 'ec2-user'  // or 'ubuntu' for Ubuntu instances
```

### Commit and Push Changes

```bash
git add Jenkinsfile
git commit -m "Update Jenkinsfile with actual values"
git push
```

---

## 6️⃣ Create Jenkins Pipeline Job

### Create New Pipeline

1. Jenkins Dashboard → **New Item**
2. Enter name: `CICD-Demo-Pipeline`
3. Select: **Pipeline**
4. Click **OK**

### Configure Pipeline

**General Section:**

- Description: `Complete CI/CD Pipeline for Flask Application`
- ✅ GitHub project
- Project url: `https://github.com/YOUR_USERNAME/Complete_CICD_Pipeline/`

**Build Triggers:**

- ✅ GitHub hook trigger for GITScm polling

**Pipeline Section:**

- Definition: `Pipeline script from SCM`
- SCM: `Git`
- Repository URL: `https://github.com/YOUR_USERNAME/Complete_CICD_Pipeline.git`
- Credentials: `git_credentials` (if private repo)
- Branch Specifier: `*/main`
- Script Path: `Jenkinsfile`

Click **Save**

---

## 7️⃣ Run Pipeline

### First Manual Run

1. Go to pipeline dashboard
2. Click **Build Now**
3. Monitor progress in **Build History**
4. Click on build number → **Console Output** to view logs

### Expected Output

```
✅ Checkout - SUCCESS
✅ Install Dependencies - SUCCESS
✅ Run Tests - SUCCESS
✅ Build Docker Image - SUCCESS
✅ Push to Registry - SUCCESS
✅ Deploy to EC2 - SUCCESS
✅ Verify Deployment - SUCCESS
✅ Cleanup Local Images - SUCCESS
```

---

## 8️⃣ Verification Steps

### Test Application Endpoints

```bash
# Health check
curl http://YOUR_EC2_IP:5000/health

# Expected response:
# {"status":"healthy","service":"cicd-demo-app","timestamp":"..."}

# Info endpoint
curl http://YOUR_EC2_IP:5000/info

# Home page (in browser)
http://YOUR_EC2_IP:5000
```

### Verify Docker Container on EC2

```bash
ssh -i your-key.pem ec2-user@YOUR_EC2_IP

# Check running containers
docker ps

# Expected output:
# CONTAINER ID   IMAGE                    STATUS    PORTS
# xxxxxxxxxxxx   cicd-demo-app:latest    Up...     0.0.0.0:5000->5000/tcp

# Check logs
docker logs cicd-demo-app

# Check container health
docker inspect cicd-demo-app | grep Health -A 5
```

### Verify on Docker Hub

1. Login to Docker Hub
2. Go to repositories
3. Verify `cicd-demo-app` exists with tags

---

## 9️⃣ Troubleshooting Guide

### Pipeline Fails at Checkout

**Error**: Authentication failed
**Solution**:

```bash
# Check git credentials in Jenkins
# For public repos, credentials not needed
# For private repos, ensure PAT is valid
```

### Pipeline Fails at Test Stage

**Error**: pytest not found
**Solution**:

```bash
# SSH to Jenkins server
# Verify Python and pip installed
python3 --version
pip3 --version

# Install if missing
sudo apt install python3-pip -y
```

### Pipeline Fails at Docker Build

**Error**: Cannot connect to Docker daemon
**Solution**:

```bash
# On Jenkins server
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
sudo systemctl restart docker
```

### Pipeline Fails at Push Image

**Error**: Authentication required
**Solution**:

```bash
# Verify Docker Hub credentials in Jenkins
# Credential ID must match: 'registry_creds'
# Try logging in manually on Jenkins server
docker login
```

### Pipeline Fails at Deploy

**Error**: SSH connection refused
**Solution**:

```bash
# Check security group allows SSH
# Verify SSH key in Jenkins credentials
# Test manual SSH
ssh -i key.pem ec2-user@YOUR_EC2_IP

# Check EC2 is running
# Verify correct username (ec2-user vs ubuntu)
```

### Application Not Accessible

**Error**: Connection timeout
**Solution**:

```bash
# Check security group allows port 5000
# Verify container is running on EC2
docker ps

# Check container logs
docker logs cicd-demo-app

# Verify app is listening
curl localhost:5000 (from inside EC2)
```

---

## 🔟 Maintenance Procedures

### Update Application Code

```bash
# Make changes to app.py
# Commit and push
git add .
git commit -m "Update application"
git push

# Pipeline automatically triggers (if webhook configured)
# Or manually trigger in Jenkins
```

### Rollback to Previous Version

```bash
# SSH to EC2
ssh -i key.pem ec2-user@YOUR_EC2_IP

# List available images
docker images

# Stop current container
docker stop cicd-demo-app
docker rm cicd-demo-app

# Run previous version
docker run -d --name cicd-demo-app -p 5000:5000 \
  YOUR_DOCKERHUB_USERNAME/cicd-demo-app:PREVIOUS_TAG
```

### Clean Up EC2 Resources

```bash
# SSH to EC2
ssh -i key.pem ec2-user@YOUR_EC2_IP

# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -a -f

# Remove unused volumes
docker volume prune -f
```

### View Application Logs

```bash
# Real-time logs
docker logs -f cicd-demo-app

# Last 100 lines
docker logs --tail 100 cicd-demo-app

# Logs with timestamps
docker logs -t cicd-demo-app
```

---

## 📸 Screenshots to Capture

For submission/documentation, capture:

1. **Jenkins Pipeline Success**
   - Full pipeline view showing all green stages
   - Console output showing "Pipeline completed successfully"

2. **Application Running**
   - Browser showing app at `http://EC2_IP:5000`
   - Health endpoint response
   - Info endpoint response

3. **Docker Hub**
   - Repository showing pushed images with tags

4. **EC2 Container**
   - `docker ps` output showing running container
   - `docker logs` output

5. **Test Coverage Report**
   - HTML coverage report from Jenkins

---

## 📞 Support

For issues or questions:

- Check Jenkins console logs
- Review EC2 container logs
- Verify all credentials are correct
- Ensure security groups allow required traffic

---

**Last Updated**: 2026-02-15
