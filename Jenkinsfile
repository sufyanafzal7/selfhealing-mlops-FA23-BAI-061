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

                    # Kill any lingering test engines on port 5000 to prevent collisions
                    pkill -f "app.py" || true
                    rm -f /tmp/app_test.log

                    cd /DevOps/app
                    export JENKINS_NODE_COOKIE=dontKillMe

                    # Start Flask locally on Port 5000 for verification testing
                    nohup /DevOps/monitoring/venv/bin/python app.py > /tmp/app_test.log 2>&1 &

                    # Give the server ample time to download/initialize the pipeline
                    sleep 15

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
                // Use your pre-configured Jenkins text credential ID for safe injection
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
                echo 'Deploying resources to Minikube cluster...'
                sh '''
                    # Direct kubectl to use the authenticated cluster configuration mapping
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
