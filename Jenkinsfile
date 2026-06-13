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
                    /DevOps/monitoring/venv/bin/python -m pytest /DevOps/tests/test_app.py
                '''
            }
        }
        stage('UI Test') {
            steps {
                echo 'Running headless Selenium browser tests...'
                sh '''
                    cd /DevOps/app
                    nohup /DevOps/monitoring/venv/bin/python app.py > /tmp/app_test.log 2>&1 &
                    sleep 5
                    /DevOps/monitoring/venv/bin/python -m pytest /DevOps/tests/test_ui.py
                    pkill -f "python app.py" || true
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
