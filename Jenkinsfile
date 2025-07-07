pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "78.46.145.88:5000/django-app-deploy:${BUILD_NUMBER}" // Make sure port matches Nexus registry
        BRANCH_NAME = 'dev' // Set your branch here
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
                    sh '''
                    echo "$DOCKER_PASS" | docker login 78.46.145.88:5000 -u "$DOCKER_USER" --password-stdin
                    docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    def namespace = ''
                    if (BRANCH_NAME == 'dev') {
                        namespace = 'dev'
                    } else if (BRANCH_NAME == 'test') {
                        namespace = 'test'
                    } else if (BRANCH_NAME == 'main') {
                        namespace = 'prod'
                    }

                    // ✅ Use kubeconfig as a temporary file
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                        sh """
                        kubectl --kubeconfig=$KUBECONFIG_FILE set image deployment/${JOB_NAME} ${JOB_NAME}=$DOCKER_IMAGE -n ${namespace} || \
                        kubectl --kubeconfig=$KUBECONFIG_FILE apply -f kubernetes/${namespace} -n ${namespace}
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
