pipeline {
    agent any

    environment {
        // Pull secrets from Jenkins credential store — never from git
        MYSQL_ROOT_PASSWORD = credentials('MYSQL_ROOT_PASSWORD')
        MYSQL_DATABASE      = credentials('MYSQL_DATABASE')
        MYSQL_USER          = credentials('MYSQL_USER')
        MYSQL_PASSWORD      = credentials('MYSQL_PASSWORD')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Write .env') {
            steps {
                // Write the .env file on the server — it never touches git
                sh '''
                    cat > .env << EOF
MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
MYSQL_DATABASE=${MYSQL_DATABASE}
MYSQL_USER=${MYSQL_USER}
MYSQL_PASSWORD=${MYSQL_PASSWORD}
EOF
                    chmod 600 .env
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose build --no-cache'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    sudo docker compose down --remove-orphans || true
                    sudo docker compose up -d
                '''
            }
        }

        stage('Health check') {
            steps {
                // Give containers 20s to start, then verify
                sh '''
                    sleep 20
                    curl -f http://localhost:5000/health || exit 1
                '''
            }
        }
    }

    post {
        always {
            // Remove the .env from Jenkins workspace after deploy
            sh 'rm -f .env'
        }
        failure {
            echo 'Pipeline failed — check logs above'
        }
    }
}