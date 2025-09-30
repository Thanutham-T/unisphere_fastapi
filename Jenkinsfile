pipeline {
    agent none

    environment {
        APP_DIR = './unisphere'
        SONARQUBE = credentials('sonarq-token')
        DOCKERHUB_REPO = "thanutham/unisphere_fastapi"
    }

    stages {
        stage('Checkout for CI') {
            agent { label 'agent-ci' }
            steps {
                git branch: 'main', url: 'https://github.com/Thanutham-T/unisphere_fastapi.git'
            }
        }
        
        stage('Set Version Tag') {
            agent { label 'agent-ci' }
            steps {
                script {
                    env.VERSION_TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    echo "VERSION_TAG = ${env.VERSION_TAG}"
                }
            }
        }

        stage('Build test image with .env') {
            agent { label 'agent-ci' }
            steps {
               withCredentials([file(credentialsId: 'env-development', variable: 'SECRET_ENV_FILE')]) {
                    sh '''
                        docker build --network=host -t unisphere:test -f Dockerfile.test .
                        cp "$SECRET_ENV_FILE" ./.devcontainer/.env.dev
                    '''
                }
            }
        }

        stage('Run Tests & Coverage') {
            agent { label 'agent-ci' }
            steps {
                sh '''
                    echo 'Environment setup...'
                    docker compose -f ./docker-compose.test.yml up -d
                    rm ./.devcontainer/.env.dev
                '''
            }
        }
        
        stage('Run SonarQube') {
            agent { label 'agent-ci' }
            environment {
                SCANNER_HOME = tool 'sonar-scanner'
            }

            steps {
                withSonarQubeEnv('sonar-server') {
                    sh '''
                        ${SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=unisphere \
                        -Dsonar.projectName=unisphere \
                        -Dsonar.sources=./${APP_DIR}/
                    '''
                }
            }
        }
        

        stage('Quality Gate') {
            agent { label 'agent-ci' }
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Build production docker image') {
            agent { label 'agent-ci' }
            steps {
                    sh 'docker build --network=host -t $DOCKERHUB_REPO:$VERSION_TAG -f Dockerfile.prod .'
            }
        }
        
        stage('Push docker image to docker hub') {
            agent { label 'agent-ci' }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "Logging into Docker Hub..."
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $DOCKERHUB_REPO:$VERSION_TAG
                        docker logout
                    '''
                }
            }
        }

        stage('Approval') {
            steps {
                script {
                    input message: 'Proceed with deployment?'
                }
            }
        }

        
        stage('Checkout for CD') {
            agent { label 'agent-cd' }
            steps {
                git branch: 'main', url: 'https://github.com/Thanutham-T/unisphere_fastapi.git'
            }
        }

        stage('Setup production environment') {
            agent { label 'agent-cd'}
            steps {
                withCredentials([file(credentialsId: 'env-production', variable: 'SECRET_ENV_FILE')]) {
                    sh '''
                        cp "$SECRET_ENV_FILE" ./.env.prod 
                    '''
                }
                withCredentials([file(credentialsId: 'redisdb-config', variable: 'SECRET_CONF_FILE')]) {
                    sh '''
                        mkdir -p dbconfig
                        cp "$SECRET_CONF_FILE" ./dbconfig/redis.conf
                    '''
                }
            }
        }

        stage('Build nginx') {
            agent { label 'agent-cd' }
            steps {
                sh 'docker build -t nginx:custom -f Dockerfile.nginx .'
            }
        }

        stage('Deploy Container') {
            agent { label 'agent-cd' }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "Logging into Docker Hub..."
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker compose --env-file ./.env.prod -f ./docker-compose.prod.yml up -d --scale unisphere-prod=2
                        docker logout
                        rm ./.env.prod
                        rm ./dbconfig/redis.conf
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished"
        }
    }
}