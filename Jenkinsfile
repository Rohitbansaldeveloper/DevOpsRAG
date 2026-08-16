pipeline {

    agent any

    environment {
        IMAGE_NAME = "devopsrag-api"
        IMAGE_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = "devopsrag-api"
        HOST_PORT = "8000"
        CONTAINER_PORT = "8000"
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

                    echo "RAG files:"
                    ls -la backend/app/rag
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running application tests...'

                sh '''
                    python3 --version
                    python3 -m py_compile backend/app/main.py
                    python3 -m py_compile backend/app/rag/*.py
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

        stage('Stop Old Container') {
            steps {
                echo 'Stopping old container if it exists...'

                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                """
            }
        }

        stage('Run Container') {
            steps {
                echo 'Starting new DevOpsRAG container...'

                sh """
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${HOST_PORT}:${CONTAINER_PORT} \
                        -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
                        -e LLM_MODEL=llama3.2 \
                        -e PROJECT_ROOT=/app \
                        --add-host=host.docker.internal:host-gateway \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Container Test') {
            steps {
                echo 'Testing running container...'

                sh '''
                    sleep 10

                    docker ps

                    curl -f http://127.0.0.1:8000/health
                '''
            }
        }
    }

    post {

        success {
            echo 'DevOpsRAG CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'DevOpsRAG pipeline failed!'
        }

        always {
            echo 'Pipeline finished.'

            sh '''
                echo "Docker containers:"
                docker ps -a

                echo "DevOpsRAG logs:"
                docker logs devopsrag-api 2>/dev/null || true
            '''
        }
    }
}
