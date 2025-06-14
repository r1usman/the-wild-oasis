pipeline {
    agent any

    stages {
        stage('Delete PHP folder if it exists') {
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

        stage('Fetch Application Code') {
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

        stage('Run Selenium Tests') {
    steps {
        dir('/var/lib/jenkins/DevOps/') {
            sh '''
                # Clean previous test folder
                rm -rf tests

                # Clone test repo
                git clone https://github.com/YOUR_USERNAME/YOUR_TEST_REPO.git tests

                # Run tests inside Selenium + Chrome container
                docker run --rm -v "$PWD/tests":/tests -w /tests python:3.12-slim /bin/bash -c "
                    apt update &&
                    apt install -y curl unzip chromium-driver chromium &&
                    pip install -r requirements.txt &&
                    pytest --maxfail=1 --disable-warnings -v
                "
            '''
        }
    }
}

    }
}
