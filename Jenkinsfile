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
                        set -xe

                        echo "=== DEBUG: Checking variables ==="
                        echo "EC2_HOST is: $EC2_HOST"
                        echo "DOCKER_USER is: $dockeruser"
                        echo "SSH_KEY file: $SSH_KEY"

                        if [ -z "$EC2_HOST" ]; then
                            echo "ERROR: EC2_HOST is empty! Check Jenkins credentials."
                            exit 1
                        fi

                        echo "=== Setting up SSH key ==="
                        chmod 600 $SSH_KEY

                        echo "=== Testing SSH connectivity to $EC2_HOST ==="
                        ssh -i $SSH_KEY \
                            -o StrictHostKeyChecking=no \
                            -o ConnectTimeout=30 \
                            ubuntu@$EC2_HOST "echo SSH connection successful"

                        echo "=== Running deployment ==="
                        ssh -i $SSH_KEY \
                            -o StrictHostKeyChecking=no \
                            -o ConnectTimeout=30 \
                            ubuntu@$EC2_HOST \
                            "echo $dockerpassword | docker login -u $dockeruser --password-stdin \
                            && docker pull $dockeruser/jenkins-lab:latest \
                            && docker stop jenkins-lab || true \
                            && docker rm jenkins-lab || true \
                            && docker run -d --name jenkins-lab -p 5000:5000 $dockeruser/jenkins-lab:latest \
                            && echo Deployment complete"

                        echo "=== Deployment done ==="
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