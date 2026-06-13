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
                echo 'Running PyTest units...'
                sh '''
                    /DevOps/monitoring/venv/bin/python -m pip install -r /DevOps/app/requirements.txt
                    /DevOps/monitoring/venv/bin/python -m pytest /DevOps/tests/test_app.py
                '''
            }
        }
        stage('UI Test') {
            steps {
                echo 'Running headless Selenium browser tests...'
                sh '''
                    /DevOps/monitoring/venv/bin/python -m pip install -r /DevOps/app/requirements.txt
                    cd /DevOps/app
                    
                    # Prevent Jenkins from killing our background Flask server
                    export JENKINS_NODE_COOKIE=dontKillMe
                    
                    # Start Flask using the absolute venv python binary path
                    nohup /DevOps/monitoring/venv/bin/python app.py > /tmp/app_test.log 2>&1 &
                    
                    # Give the server ample time to download/load the sentiment model weights
                    sleep 12
                    
                    # Check if the app crashed early, and print logs if it did
                    if ! pgrep -f "app.py" > /dev/null; then
                        echo "=== APPLICATION CRASHED EARLY. LOGS BELOW ==="
                        cat /tmp/app_test.log
                        exit 1
                    fi
                    
                    /DevOps/monitoring/venv/bin/python -m pytest /DevOps/tests/test_ui.py
                    pkill -f "app.py" || true
                '''
            }
        }
        stage('Build and Push') {
            steps {
                echo 'Pushing images to DockerHub...'
                sh '''
                    cd app
                    docker tag ${DOCKER_USER}/${APP_NAME}:unstable ${DOCKER_USER}/${APP_NAME}:stable
                    docker push ${DOCKER_USER}/${APP_NAME}:unstable
                    docker push ${DOCKER_USER}/${APP_NAME}:stable
                '''
            }
        }
        stage('Deploy to Minikube') {
            steps {
                echo 'Deploying resources to Minikube cluster...'
                sh '''
                    kubectl apply -f k8s/pvc.yaml
                    kubectl apply -f k8s/blue-deployment.yaml
                    kubectl apply -f k8s/green-deployment.yaml
                    kubectl apply -f k8s/service.yaml
                '''
            }
        }
    }
}
