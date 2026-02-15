#!/bin/bash

###############################################################################
# EC2 Deployment Script for CI/CD Demo Application
# This script pulls the latest Docker image and deploys it on EC2
###############################################################################

set -e  # Exit on any error

# Configuration
CONTAINER_NAME="cicd-demo-app"
APP_PORT=5000

# These should be passed as environment variables from Jenkins
DOCKER_IMAGE=${DOCKER_IMAGE:-"YOUR_DOCKERHUB_USERNAME/cicd-demo-app"}
IMAGE_TAG=${IMAGE_TAG:-"latest"}
DOCKER_USER=${DOCKER_USER:-""}
DOCKER_PASS=${DOCKER_PASS:-""}

echo "=================================================="
echo "Starting deployment process..."
echo "Image: ${DOCKER_IMAGE}:${IMAGE_TAG}"
echo "=================================================="

# Login to Docker Hub
if [ -n "$DOCKER_USER" ] && [ -n "$DOCKER_PASS" ]; then
    echo "Logging into Docker registry..."
    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
else
    echo "Warning: Docker credentials not provided"
fi

# Pull the latest image
echo "Pulling Docker image..."
docker pull ${DOCKER_IMAGE}:${IMAGE_TAG}

# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "Stopping existing container..."
    docker stop ${CONTAINER_NAME} || true
    echo "Removing existing container..."
    docker rm ${CONTAINER_NAME} || true
fi

# Run the new container
echo "Starting new container..."
docker run -d \
    --name ${CONTAINER_NAME} \
    --restart unless-stopped \
    -p ${APP_PORT}:5000 \
    -e APP_VERSION="${IMAGE_TAG}" \
    -e ENVIRONMENT="production" \
    ${DOCKER_IMAGE}:${IMAGE_TAG}

# Wait for container to be healthy
echo "Waiting for application to start..."
sleep 5

# Verify container is running
if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    echo "✅ Container is running successfully!"
    docker ps -f name=${CONTAINER_NAME}
else
    echo "❌ Container failed to start!"
    docker logs ${CONTAINER_NAME}
    exit 1
fi

# Test health endpoint
echo "Testing health endpoint..."
if curl -f http://localhost:${APP_PORT}/health; then
    echo "✅ Application is healthy!"
else
    echo "❌ Health check failed!"
    exit 1
fi

# Cleanup old images (keep last 3 versions)
echo "Cleaning up old Docker images..."
docker image prune -f

# Remove dangling images
OLD_IMAGES=$(docker images -f "dangling=true" -q)
if [ -n "$OLD_IMAGES" ]; then
    echo "Removing dangling images..."
    docker rmi $OLD_IMAGES || true
fi

# Keep only the last 3 tagged versions of our image
echo "Removing old versions (keeping last 3)..."
docker images ${DOCKER_IMAGE} --format "{{.Tag}}" | \
    grep -v "latest" | \
    tail -n +4 | \
    xargs -I {} docker rmi ${DOCKER_IMAGE}:{} 2>/dev/null || true

echo "=================================================="
echo "Deployment completed successfully!"
echo "Application available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):${APP_PORT}"
echo "=================================================="
