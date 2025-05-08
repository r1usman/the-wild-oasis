pipeline {
    agent any

    stages {
        stage('Cleanup Docker and free DevOps folder') {
            steps {
                sh 'docker system prune -af' 
                sh 'rm -r /var/lib/jenkins/DevOps/*'

            }
        }
        
        stage('Fetch code ') {
            steps {
                sh 'git clone https://github.com/r1usman/upizza.git /var/lib/jenkins/DevOps/php/'
            }
        }

        stage('Build and Start Docker Compose') {
            steps {
                dir('/var/lib/jenkins/DevOps/php/') {
                    sh 'docker compose up -d'
                }
            }
        }
    }

}
