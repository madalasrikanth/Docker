pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t banking-app:latest .'
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker stop banking-container || true
                    docker rm banking-container || true

                    docker run -d \
                      --restart unless-stopped \
                      --name banking-container \
                      -p 8000:8000 \
                      banking-app:latest
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    sleep 5
                    docker ps --filter name=banking-container
                    docker logs --tail 20 banking-container
                    curl --fail --retry 5 --retry-delay 2 \
                      http://127.0.0.1:8000/
                '''
            }
        }
    }
}
