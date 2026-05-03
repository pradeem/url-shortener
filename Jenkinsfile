pipeline {
    agent any

    environment {
        IMAGE = "pradeem/url-shortener:latest"
    }

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/pradeem/url-shortener.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push $IMAGE'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                    kubectl apply -f k8s/
                    kubectl rollout status deployment/url-shortener
                    '''
                }
        }
    }
}