pipeline {
    agent any

    stages {
        stage('delete php folder if it exists') {
            steps {
               sh '''
            if [ -d "/var/lib/jenkins/DevOps/" ]; then
                find "/var/lib/jenkins/DevOps/" -mindepth 1 -delete
                echo "Contents of /var/lib/jenkins/DevOps/ have been removed."
            else
                echo "Directory /var/lib/jenkins/DevOps/ does not exist."
            fi
        '''

            }
        }
        
        stage('Fetch code ') {
            steps {
                sh 'git clone https://github.com/r1usman/the-wild-oasis.git /var/lib/jenkins/DevOps/php/'
            }
        }

        stage('Build and Start Docker Compose') {
            steps {
                dir('/var/lib/jenkins/DevOps/php/') {
                    sh 'docker compose -p thereactapp up -d'
                }
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'python:3.9-slim'
                }
            }
            steps {
                script {
                    sh 'python --version'

                    // Install Google Chrome and WebDriver
                    sh """
                        apt-get update && apt-get install -y wget unzip gnupg
                        wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
                        sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
                        apt-get update
                        apt-get install -y google-chrome-stable
                        wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/126.0.6478.61/linux64/chromedriver-linux64.zip
                        unzip /tmp/chromedriver.zip -d /usr/bin
                        mv /usr/bin/chromedriver-linux64/chromedriver /usr/bin/chromedriver
                        chmod +x /usr/bin/chromedriver
                    """

                    // Install Python dependencies from your requirements file
                    sh 'pip install -r requirements.txt'

                    // Run ALL tests found by pytest in the directory
                    echo 'Running all Selenium tests...'
                    sh 'pytest -v'
                }
            }
        }
    }

}
