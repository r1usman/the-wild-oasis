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

        // --- CORRECTED TESTING PROCESS (SPLIT INTO TWO STAGES) ---

        // Stage 4: Download the test code to the Jenkins host machine
        stage('Checkout Test Code') {
            steps {
                script {
                    def testDir = "/var/lib/jenkins/DevOps/tests"
                    sh "rm -rf ${testDir} && mkdir -p ${testDir}"
                    
                    echo "Fetching test code from separate repository..."
                    // *** IMPORTANT: Change this URL to your test repository ***
                    sh "git clone https://github.com/r1usman/test-cases.git ${testDir}"
                }
            }
        }

        // Stage 5: Run the tests from inside a clean Docker environment
        // Stage 5: Run the tests from inside a clean Docker environment
        stage('Execute Automated Tests') {
            // The agent is correctly defined at the top of the stage
            agent {
                docker {
                    image 'python:3.9-slim'
                    args '--network host'
                    // This mounts the test directory from the host into the container
                    args '-v /var/lib/jenkins/DevOps/tests:/tests'
                }
            }
            steps {
                // Change directory to the mounted test code inside the container
                dir('/tests') {
                    echo 'Setting up the testing environment...'

                    // This multi-line sh block will now execute correctly
                    sh """
                        set -e
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

                    // Run the tests
                    echo 'Running Selenium tests...'
                    sh 'pytest -v'
                }
            }
        }
    }
    
    // --- CLEANUP BLOCK (UNCHANGED) ---
    post {
        always {
            echo 'Stopping the Docker Compose application...'
            dir('/var/lib/jenkins/DevOps/php/') {
                sh 'docker compose -p thereactapp down'
            }
            echo 'Pipeline finished.'
        }
    }
}