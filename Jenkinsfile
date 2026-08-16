pipeline {

    agent any

    environment {
        IMAGE_NAME = "devopsrag-api"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Verify Project') {
            steps {
                echo 'Checking project structure...'

                sh '''
                    echo "Current directory:"
                    pwd

                    echo "Project files:"
                    ls -la

                    echo "Backend:"
                    ls -la backend
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running application tests...'

                sh '''
                    python3 --version
                    python3 -m py_compile backend/app/main.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'

                sh """
                    docker build \
                        -f backend/Dockerfile \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        .
                """
            }
        }

        stage('Docker Image Test') {
            steps {
                echo 'Checking Docker image...'

                sh """
                    docker images ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }

    post {

        success {
            echo 'DevOpsRAG CI pipeline completed successfully!'
        }

        failure {
            echo 'DevOpsRAG CI pipeline failed!'
        }

        always {
            echo 'Pipeline finished.'
        }
    }
}
