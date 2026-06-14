pipeline {
    agent any

    environment {
        DOCKER_USER = 'sufyanafzal7'
        APP_NAME    = 'sentiment-api'
    }

    stages {
        stage('Fetch') {
            steps {
                echo 'Pulling code from GitHub...'
                checkout scm
            }
        }
        stage('Build and Run') {
            steps {
                echo 'Building and running unstable Docker container...'
                sh 'cd app && docker build -t ${DOCKER_USER}/${APP_NAME}:unstable .'
            }
        }
        stage('Unit Test') {
            steps {
                echo 'Starting application container context for API unit evaluations...'
                sh '''
                    # Stop and clear any existing test container to ensure a clean slate
                    docker rm -f sentiment-api-test || true

                    # Run the container built in the previous stage, mapping the HuggingFace cache directory
                    docker run -d -p 5000:5000 --name sentiment-api-test -v /DevOps/hf_cache:/root/.cache/huggingface ${DOCKER_USER}/${APP_NAME}:unstable
                    
                    # Give the container's native, supported Python 3.10 environment time to map model weights
                    sleep 30

                    # Run pytest from the host's lightweight venv against the live container port
                    /DevOps/monitoring/venv/bin/python -m pytest /DevOps/tests/test_api.py
                '''
            }
        }
        stage('UI Test') {
            steps {
                echo 'Running headless Selenium browser tests against active container context...'
                sh '''
                    # Execute your UI tests against the active container port
                    /DevOps/monitoring/venv/bin/python -m pytest /DevOps/tests/test_ui.py
                    
                    # Tear down and clean up the test container cleanly
                    docker rm -f sentiment-api-test || true
                '''
            }
        }
        stage('Build and Push') {
            steps {
                echo 'Pushing images to DockerHub registries...'
                withCredentials([string(credentialsId: 'dockerhub-token', variable: 'DOCKER_TOKEN')]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                        cd app
                        docker tag ${DOCKER_USER}/${APP_NAME}:unstable ${DOCKER_USER}/${APP_NAME}:stable
                        docker push ${DOCKER_USER}/${APP_NAME}:unstable
                        docker push ${DOCKER_USER}/${APP_NAME}:stable
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                echo 'Deploying resources to Minikube cluster layers...'
                sh '''
                    export KUBECONFIG=/home/ubuntu/.kube/config
                    kubectl apply -f k8s/pvc.yaml
                    kubectl apply -f k8s/blue-deployment.yaml
                    kubectl apply -f k8s/green-deployment.yaml
                    kubectl apply -f k8s/service.yaml
                '''
            }
        }
    }
}

