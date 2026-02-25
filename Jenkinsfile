pipeline {
    agent any

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
                    python3 -m venv venv
                    . venv/bin/activate
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests with coverage...'
                sh '''
                    . venv/bin/activate
                    python3 -m pytest test_app.py -v --cov=app --cov-report=term-missing --cov-report=html
                '''
            }
            post {
                always {
                    echo 'Archiving test coverage report...'
                    archiveArtifacts artifacts: 'htmlcov/**', allowEmptyArchive: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                withCredentials([
                    usernamePassword(
                        credentialsId: 'Docker-hub',
                        passwordVariable: 'dockerpassword',
                        usernameVariable: 'dockeruser'
                    )
                ]) {
                    sh '''
                        docker build -t $dockeruser/jenkins-lab:latest .
                        echo "$dockerpassword" | docker login -u "$dockeruser" --password-stdin
                        docker push $dockeruser/jenkins-lab:latest
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo 'Deploying to EC2 instance (eu-central-1 Frankfurt)...'
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'jenkins-ec2',
                        keyFileVariable: 'SSH_KEY'
                    ),
                    usernamePassword(
                        credentialsId: 'Docker-hub',
                        passwordVariable: 'dockerpassword',
                        usernameVariable: 'dockeruser'
                    ),
                    string(credentialsId: 'EC2_HOST', variable: 'EC2_HOST')
                ]) {
                    sh '''
                        chmod 600 $SSH_KEY

                        # Copy deploy script to EC2 instance
                        scp -i $SSH_KEY -o StrictHostKeyChecking=no \
                            scripts/deploy.sh ubuntu@$EC2_HOST:/home/ubuntu/deploy.sh

                        # Make it executable and run it with required env vars
                        ssh -i $SSH_KEY -o StrictHostKeyChecking=no ubuntu@$EC2_HOST \
                            "chmod +x /home/ubuntu/deploy.sh && \
                             DOCKER_IMAGE=$dockeruser/jenkins-lab \
                             IMAGE_TAG=latest \
                             DOCKER_USER=$dockeruser \
                             DOCKER_PASS=$dockerpassword \
                             /home/ubuntu/deploy.sh"
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Verifying application is running...'
                withCredentials([string(credentialsId: 'EC2_HOST', variable: 'EC2_HOST')]) {
                    script {
                        sleep(time: 15, unit: 'SECONDS')
                        sh '''
                            curl -f http://$EC2_HOST:5000/health || exit 1
                            echo "Application is healthy!"
                        '''
                    }
                }
            }
        }

        stage('Cleanup Local Images') {
            steps {
                echo 'Cleaning up local Docker images...'
                withCredentials([
                    usernamePassword(
                        credentialsId: 'Docker-hub',
                        passwordVariable: 'dockerpassword',
                        usernameVariable: 'dockeruser'
                    )
                ]) {
                    sh '''
                        docker rmi $dockeruser/jenkins-lab:latest || true
                        docker image prune -f
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
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