pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "78.46.145.88:5000/django-app-deploy:${BUILD_NUMBER}"
        BRANCH_NAME = 'dev'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'dev', url: 'https://github.com/Silkensway-Clothing/silkensway_clothing.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t $DOCKER_IMAGE ."
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                    echo "$DOCKER_PASS" | docker login 78.46.145.88:5000 -u "$DOCKER_USER" --password-stdin
                    docker push $DOCKER_IMAGE
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                    script {
                        def namespace = BRANCH_NAME
                        sh """
                        export KUBECONFIG=${KUBECONFIG_FILE}
                        kubectl get pods -n ${namespace}
                        kubectl set image deployment/django-app-deploy django-app-deploy=$DOCKER_IMAGE -n ${namespace} || \
                        kubectl apply -f kubernetes/${namespace} -n ${namespace} --validate=false
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
