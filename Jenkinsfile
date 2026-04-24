pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t 2024ht66055 .'
            }
        }

        stage('Run Tests in Docker') {
            steps {
                sh 'docker run --rm 2024ht66055 pytest'
            }
        }
    }
}
