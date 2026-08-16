
pipeline {

    agent any

    environment {
        IMAGE_NAME = "rohitbansal2113/devopsrag-api"
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
                    docker build -f backend/Dockerfile -t ${IMAGE_NAME}:${IMAGE_TAG} .
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
                    docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} -v devopsrag_vectorstore:/app/vectorstore -e OLLAMA_BASE_URL=http://host.docker.internal:11434 -e LLM_MODEL=llama3.2 -e PROJECT_ROOT=/app --add-host=host.docker.internal:host-gateway ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Container Test') {
            steps {
                echo 'Testing running container...'

                sh '''
                    echo "Checking container status..."
                    docker ps

                    echo "Waiting for FastAPI..."

                    for i in $(seq 1 12)
                    do
                        echo "Health check attempt $i..."

                        if curl -fsS http://127.0.0.1:8000/health; then
                            echo ""
                            echo "DevOpsRAG API is healthy!"
                            exit 0
                        fi

                        echo "API not ready yet. Waiting 5 seconds..."
                        sleep 5
                    done

                    echo "ERROR: DevOpsRAG API did not become healthy."

                    echo "Container logs:"
                    docker logs devopsrag-api

                    exit 1
                '''
            }
        }

        stage('Docker Login') {
            steps {
                echo 'Logging into Docker Hub...'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            --username "$DOCKER_USERNAME" \
                            --password-stdin
                    '''
                }
            }
        }

        stage('Docker Push') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'

                sh """
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
    }
        stage('Deploy to Kubernetes') {
             steps {
                 echo "Deploying ${IMAGE_NAME}:${IMAGE_TAG} to Kubernetes..."

                 sh '''
                      kubectl apply -f k8s/namespace.yaml
                      kubectl set image deployment/devopsrag-api \
                        devopsrag-api=${IMAGE_NAME}:${IMAGE_TAG} \
                         -n devopsrag
                      kubectl apply -f k8s/service.yaml
                 '''
           }
       }
         stage('Verify Kubernetes Deployment') {
             steps {
                 echo 'Waiting for Kubernetes rollout...'

                 sh '''
                     kubectl rollout status deployment/devopsrag-api \
                         -n devopsrag \
                         --timeout=180s

                     echo "Pods:"
                     kubectl get pods -n devopsrag

                     echo "Deployment:"
                     kubectl get deployment devopsrag-api -n devopsrag

                     echo "Service:"
                     kubectl get service devopsrag-service -n devopsrag

                 '''
           }
       }  
    post {

        success {
            echo 'DevOpsRAG CI/CD pipeline completed successfully!'
            echo "Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
        }

        failure {
            echo 'DevOpsRAG CI/CD pipeline failed!'
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
