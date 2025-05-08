pipeline {
    agent any

    stages {
        stage('Cleanup Docker and free DevOps folder') {
            steps {
                sh 'docker system prune -af' 
               sh '''
            if [ -d "/var/lib/jenkins/DevOps/" ]; then
                rm -r "/var/lib/jenkins/DevOps/"
                echo "Directory /var/lib/jenkins/DevOps/ has been removed."
            else
                echo "Directory /var/lib/jenkins/DevOps/ does not exist."
            fi
        '''

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
