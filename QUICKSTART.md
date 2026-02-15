# 🚀 Quick Setup Guide

## Repository Information

- **GitHub URL**: https://github.com/valensniyonkuru/Project-Complete-CI-CD-Pipeline.git
- **Status**: ✅ Code pushed successfully
- **Commit**: 01adf0a - Initial commit: Complete CI/CD Pipeline with Flask, Docker, Jenkins
- **Files**: 11 files, 1577 lines of code

## What's Included ✅

1. **Flask Application** (`app.py`)
   - Modern glassmorphism UI
   - 3 endpoints: `/`, `/health`, `/info`
   - 6 unit tests - all passing ✅
   - 89% code coverage ✅

2. **Docker Configuration**
   - Multi-stage optimized Dockerfile
   - Security: non-root user
   - Health checks included

3. **Jenkins Pipeline** (`Jenkinsfile`)
   - 7 automated stages
   - Checkout → Build → Test → Docker → Push → Deploy → Cleanup

4. **Documentation**
   - README.md (comprehensive guide)
   - RUNBOOK.md (step-by-step operations)

## 📝 Next Steps - ACTION REQUIRED

### 1. Update Jenkinsfile (REQUIRED)

Edit `Jenkinsfile` and replace:

```groovy
DOCKER_IMAGE = 'YOUR_DOCKERHUB_USERNAME/cicd-demo-app'  ← Add your Docker Hub username
EC2_HOST = 'YOUR_EC2_PUBLIC_IP'                        ← Add your EC2 IP
EC2_USER = 'ec2-user'                                   ← Change to 'ubuntu' if using Ubuntu
```

### 2. Setup EC2 Instance

```bash
# Launch t2.micro or larger
# Configure Security Groups:
#   - SSH (22) from your IP
#   - HTTP (5000) from anywhere
#   - HTTPS (443) optional

# Connect and install Docker:
ssh -i your-key.pem ec2-user@YOUR_EC2_IP
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo usermod -aG docker ec2-user
```

### 3. Setup Jenkins

- Install Jenkins LTS
- Install required plugins (listed in README.md)
- Configure 3 credentials:
  1. `registry_creds` - Docker Hub (username + password)
  2. `ec2_ssh` - EC2 SSH key (private key)
  3. `git_credentials` - GitHub (optional for public repos)

### 4. Create Jenkins Pipeline

- New Item → Pipeline
- GitHub project: https://github.com/valensniyonkuru/Project-Complete-CI-CD-Pipeline
- Pipeline script from SCM
- Repository: https://github.com/valensniyonkuru/Project-Complete-CI-CD-Pipeline.git
- Script Path: `Jenkinsfile`

### 5. Run Pipeline

- Click "Build Now"
- Monitor console output
- Verify all stages pass ✅

### 6. Verify Deployment

```bash
# Test endpoints
curl http://YOUR_EC2_IP:5000/health
curl http://YOUR_EC2_IP:5000/info

# Open in browser
http://YOUR_EC2_IP:5000
```

### 7. Capture Screenshots (for submission)

- [ ] Jenkins pipeline success (all green)
- [ ] Application in browser
- [ ] Docker Hub showing image
- [ ] EC2 terminal with `docker ps`
- [ ] Test coverage report from Jenkins

## 📚 Key Files Reference

| File                | Purpose               |
| ------------------- | --------------------- |
| `app.py`            | Flask application     |
| `test_app.py`       | Unit tests (6 tests)  |
| `Dockerfile`        | Container definition  |
| `Jenkinsfile`       | Pipeline automation   |
| `scripts/deploy.sh` | EC2 deployment script |
| `README.md`         | Main documentation    |
| `RUNBOOK.md`        | Operations manual     |

## 🔧 Troubleshooting Commands

```bash
# Check local tests
cd Complete_CICD_Pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest test_app.py -v

# Build Docker locally
docker build -t test-app .
docker run -p 5000:5000 test-app

# Check EC2 deployment
ssh ec2-user@YOUR_EC2_IP
docker ps
docker logs cicd-demo-app
```

## 📞 Need Help?

1. Check `README.md` for detailed setup
2. Check `RUNBOOK.md` for troubleshooting
3. Review Jenkins console logs
4. Check EC2 container logs: `docker logs cicd-demo-app`

---

**Repository**: https://github.com/valensniyonkuru/Project-Complete-CI-CD-Pipeline.git
**Status**: ✅ Ready for Jenkins & EC2 setup
**Last Updated**: 2026-02-15
