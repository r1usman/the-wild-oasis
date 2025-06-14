pipeline {
    // Run all stages on any available Jenkins agent
    agent any

    stages {
        // Stage 1: Clean the workspace (a safer replacement for your delete script)
        stage('Clean Workspace') {
            steps {
                echo 'Cleaning up the workspace for a fresh run...'
                // This is the standard Jenkins way to wipe the directory before a build
                cleanWs() 
            }
        }
        
        // Stage 2: Fetch your application and test code from GitHub
        stage('Checkout Code') {
            steps {
                echo 'Fetching code from https://github.com/r1usman/the-wild-oasis.git...'
                // The standard 'git' step is cleaner and handles credentials better
                git 'https://github.com/r1usman/the-wild-oasis.git'
            }
        }

        // Stage 3: Build and start your application using Docker Compose
        stage('Build and Start Application') {
            steps {
                echo 'Starting the application via Docker Compose...'
                // The -p flag gives your docker-compose project a unique name
                // to avoid conflicts and make cleanup easier.
                sh 'docker compose -p thereactapp up -d'
            }
        }

        // Stage 4 (NEW): Run Selenium tests against the running application
        stage('Run Automated Tests') {
            // This stage runs inside a temporary Docker container for a clean test environment
            agent {
                docker {
                    image 'python:3.9-slim'
                    // CRUCIAL: Allows the container to connect to 'localhost' on the Jenkins host,
                    // where your application container is running.
                    args '--network host'
                }
            }
            steps {
                script {
                    echo 'Setting up the testing environment...'

                    // Step 4.1: Install Google Chrome and its driver inside the container
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

                    // Step 4.2: Install Python dependencies from your requirements file
                    echo 'Installing Python dependencies...'
                    sh 'pip install -r requirements.txt'

                    // Step 4.3: Run all tests using pytest
                    echo 'Running Selenium tests...'
                    sh 'pytest -v'
                }
            }
        }
    }

    // This 'post' block runs after all stages are done, ensuring proper cleanup
    post {
        always {
            // This is a critical step to stop your application and free up resources
            echo 'Stopping the Docker Compose application...'
            sh 'docker compose -p thereactapp down'
            echo 'Pipeline finished.'
        }
    }
}