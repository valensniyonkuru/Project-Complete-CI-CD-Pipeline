# Screenshots Directory

This directory contains screenshots for documentation and submission.

## Required Screenshots

1. **pipeline_success.png** - Jenkins pipeline showing all stages completed successfully
2. **app_running.png** - Browser showing the application running at http://EC2_IP:5000
3. **dockerhub_image.png** - Docker Hub showing the pushed image and tags
4. **ec2_container.png** - EC2 terminal showing `docker ps` with running container
5. **test_coverage.png** - Jenkins coverage report

## How to Capture

### Jenkins Pipeline Success

1. Run the pipeline in Jenkins
2. Once complete, take a screenshot of the pipeline view showing all green stages
3. Save as `pipeline_success.png`

### Application Running

1. Open browser to `http://YOUR_EC2_IP:5000`
2. Take screenshot of the landing page
3. Save as `app_running.png`

### Docker Hub Image

1. Login to Docker Hub
2. Navigate to your repository
3. Take screenshot showing the image with tags
4. Save as `dockerhub_image.png`

### EC2 Container

1. SSH to EC2: `ssh -i key.pem ec2-user@YOUR_EC2_IP`
2. Run: `docker ps`
3. Take screenshot showing the running container
4. Save as `ec2_container.png`

### Test Coverage

1. Open Jenkins build
2. Click on "Coverage Report"
3. Take screenshot of the HTML coverage report
4. Save as `test_coverage.png`

## Notes

- All screenshots should be in PNG format
- Make sure screenshots are clear and readable
- Include timestamps where visible
