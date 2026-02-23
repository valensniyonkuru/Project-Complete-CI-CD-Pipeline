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
                    pip install --upgrade pip
                    pip install -r requirements.txt
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
                    echo 'Archiving test results...'
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
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        passwordVariable: 'dockerpassword',
                        usernameVariable: 'dockeruser'
                    )
                ]) {
                    sh """
                        docker build -t ${dockeruser}/jenkins-lab:latest .
                        echo ${dockerpassword} | docker login -u ${dockeruser} --password-stdin
                        docker push ${dockeruser}/jenkins-lab:latest
                    """
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo 'Deploying to EC2 instance...'
                sshagent(['jenkins-ec2']) {
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'dockerhub',
                            passwordVariable: 'dockerpassword',
                            usernameVariable: 'dockeruser'
                        ),
                        string(credentialsId: 'EC2_HOST', variable: 'EC2_HOST')
                    ]) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ubuntu@${EC2_HOST} << EOF
                                echo ${dockerpassword} | docker login -u ${dockeruser} --password-stdin
                                docker pull ${dockeruser}/jenkins-lab:latest
                                docker stop jenkins-lab || true
                                docker rm jenkins-lab || true
                                docker run -d --name jenkins-lab -p 5000:5000 ${dockeruser}/jenkins-lab:latest
                            EOF
                        """
                    }
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Verifying application is running...'
                withCredentials([string(credentialsId: 'EC2_HOST', variable: 'EC2_HOST')]) {
                    script {
                        sleep(time: 10, unit: 'SECONDS')
                        sh """
                            curl -f http://${EC2_HOST}:5000/health || exit 1
                            echo "Application is healthy!"
                        """
                    }
                }
            }
        }

        stage('Cleanup Local Images') {
            steps {
                echo 'Cleaning up local Docker images...'
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        passwordVariable: 'dockerpassword',
                        usernameVariable: 'dockeruser'
                    )
                ]) {
                    sh """
                        docker rmi ${dockeruser}/jenkins-lab:latest || true
                        docker image prune -f
                    """
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