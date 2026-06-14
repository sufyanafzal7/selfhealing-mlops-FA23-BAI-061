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
                echo 'Starting application process context for API unit evaluations...'
                sh '''
                    /DevOps/monitoring/venv/bin/python -m pip install -r /DevOps/app/requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
                    pkill -f "app.py" || true
                    
                    cd /DevOps/app
                    export JENKINS_NODE_COOKIE=dontKillMe
                    nohup /DevOps/monitoring/venv/bin/python app.py > /tmp/app_test.log 2>&1 &
                    sleep 15
                    
                    /DevOps/monitoring/venv/bin/python -m pytest /DevOps/tests/test_api.py
                '''
            }
        }
        stage('UI Test') {
            steps {
                echo 'Running headless Selenium browser tests against active process context...'
                sh '''
                    /DevOps/monitoring/venv/bin/python -m pytest /DevOps/tests/test_ui.py
                    pkill -f "app.py" || true
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

