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
                    sh '''
                    echo "$DOCKER_PASS" | docker login 78.46.145.88:5000 -u "$DOCKER_USER" --password-stdin
                    docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                    script {
                        def namespace = 'dev' // Default namespace
                        if (BRANCH_NAME == 'test') {
                            namespace = 'test'
                        } else if (BRANCH_NAME == 'main') {
                            namespace = 'prod'
                        }

                        sh """
                        export KUBECONFIG=${KUBECONFIG_FILE}
                        echo "✅ Using kubeconfig: \$KUBECONFIG"
                        kubectl --insecure-skip-tls-verify=true get pods -n ${namespace} || true
                        kubectl --insecure-skip-tls-verify=true \
                        set image deployment/django-app-deploy django-app-deploy=$DOCKER_IMAGE -n ${namespace} || \
                        kubectl --insecure-skip-tls-verify=true \
                        apply -f kubernetes/${namespace} -n ${namespace} --validate=false
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
