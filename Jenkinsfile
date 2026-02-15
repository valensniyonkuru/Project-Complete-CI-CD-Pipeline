pipeline {
    agent any
    
    environment {
        // Docker Hub credentials (configure in Jenkins)
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = 'YOUR_DOCKERHUB_USERNAME/cicd-demo-app'
        DOCKER_CREDENTIALS_ID = 'registry_creds'
        
        // EC2 deployment
        EC2_HOST = 'YOUR_EC2_PUBLIC_IP'
        EC2_USER = 'ec2-user'
        EC2_SSH_CREDENTIALS_ID = 'ec2_ssh'
        
        // Git credentials (optional if public repo)
        GIT_CREDENTIALS_ID = 'git_credentials'
        
        // Build version
        BUILD_VERSION = "${env.BUILD_NUMBER}"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
                sh 'echo "Build Number: ${BUILD_NUMBER}"'
                sh 'ls -la'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 --version
                    pip3 install --user -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running unit tests with coverage...'
                sh '''
                    python3 -m pytest test_app.py -v --cov=app --cov-report=term-missing --cov-report=html
                '''
            }
            post {
                always {
                    echo 'Archiving test results...'
                    // Archive coverage reports
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    // Build with multiple tags
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} \
                                     -t ${DOCKER_IMAGE}:latest \
                                     --build-arg BUILD_VERSION=${BUILD_VERSION} .
                    """
                    sh "docker images | grep ${DOCKER_IMAGE}"
                }
            }
        }
        
        stage('Push to Registry') {
            steps {
                echo 'Pushing Docker image to registry...'
                script {
                    withCredentials([usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS_ID}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                            docker push ${DOCKER_IMAGE}:latest
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to EC2') {
            steps {
                echo 'Deploying to EC2 instance...'
                script {
                    sshagent(credentials: ["${EC2_SSH_CREDENTIALS_ID}"]) {
                        sh """
                            # Copy deployment script to EC2
                            scp -o StrictHostKeyChecking=no scripts/deploy.sh ${EC2_USER}@${EC2_HOST}:/tmp/
                            
                            # Execute deployment on EC2
                            ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} \
                                "chmod +x /tmp/deploy.sh && \
                                 DOCKER_IMAGE=${DOCKER_IMAGE} \
                                 IMAGE_TAG=${IMAGE_TAG} \
                                 DOCKER_USER=$DOCKER_USER \
                                 DOCKER_PASS='$DOCKER_PASS' \
                                 /tmp/deploy.sh"
                        """
                    }
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying application is running...'
                script {
                    sleep(time: 10, unit: 'SECONDS')
                    sh """
                        curl -f http://${EC2_HOST}:5000/health || exit 1
                        echo "Application is healthy!"
                    """
                }
            }
        }
        
        stage('Cleanup Local Images') {
            steps {
                echo 'Cleaning up local Docker images...'
                sh """
                    docker rmi ${DOCKER_IMAGE}:${IMAGE_TAG} || true
                    docker rmi ${DOCKER_IMAGE}:latest || true
                    docker image prune -f
                """
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline completed successfully!'
            echo "Application deployed: http://${EC2_HOST}:5000"
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
    }
}
