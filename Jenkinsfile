pipeline {
    agent any

    stages {
        // --- YOUR EXISTING STAGES (UNCHANGED) ---
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

        // --- NEW TESTING STAGE ---
        stage('Run Automated Tests') {
            steps {
                script {
                    // Step 1: Create a clean directory for the test code and clone it
                    def testDir = "/var/lib/jenkins/DevOps/tests"
                    sh "rm -rf ${testDir} && mkdir -p ${testDir}"
                    
                    echo "Fetching test code from separate repository..."
                    // *** IMPORTANT: Change this URL to your test repository ***
                    sh "git clone https://github.com/r1usman/test-cases.git ${testDir}"

                    // Step 2: Change into the test directory to run the tests inside Docker
                    dir(testDir) {
                        // This agent block creates a temporary Docker container just for this part
                        agent {
                            docker {
                                image 'python:3.9-slim'
                                // CRUCIAL: Allows the test container to connect to your app on localhost
                                args '--network host'
                            }
                        }
                        
                        // These steps run inside the temporary python:3.9-slim container
                        steps {
                            echo 'Setting up the testing environment...'

                            // Install Chrome browser and its driver
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

                            // Install Python dependencies
                            echo 'Installing Python dependencies...'
                            sh 'pip install -r requirements.txt'

                            // Run tests using pytest
                            echo 'Running Selenium tests...'
                            sh 'pytest -v'
                        }
                    }
                }
            }
        }
    }
    
    // --- NEW CLEANUP BLOCK ---
    // This 'post' section runs after all stages are finished, regardless of success or failure
    post {
        always {
            // This is a critical cleanup step to stop your application containers
            echo 'Stopping the Docker Compose application...'
            dir('/var/lib/jenkins/DevOps/php/') {
                sh 'docker compose -p thereactapp down'
            }
            echo 'Pipeline finished.'
        }
    }
}