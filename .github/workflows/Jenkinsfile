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
                bat 'docker build -t 2024ht66055 .'
            }
        }

        stage('Run Tests in Docker') {
            steps {
                bat 'docker run --rm 2024ht66055 pytest'
            }
        }
    }
}