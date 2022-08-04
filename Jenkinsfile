pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = '114992278129.dkr.ecr.ap-southeast-1.amazonaws.com/firehose-tracer-log'
        TAG = "${BRANCH_NAME}-${GIT_COMMIT}"
        TAG_LATEST = "${BRANCH_NAME}-latest"
    }
    stages {
        stage('Get Commit Detail') {
            steps {
                script {
                    env.GIT_COMMIT_MSG = sh (script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()
                    env.GIT_AUTHOR = sh (script: 'git log -1 --pretty=%cn ${GIT_COMMIT}', returnStdout: true).trim()
                    env.GIT_COMMIT = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                }
            }
        }
        stage('Built Image') {
            steps {
                sh """
                    docker build \
                    --no-cache  \
                    --build-arg ENVIRONMENT=${BRANCH_NAME} \
                    -t ${DOCKER_REGISTRY}:${TAG} \
                    -t ${DOCKER_REGISTRY}:${TAG_LATEST} \
                    .
                """
            }
        }
        stage('Login Registry') {
            steps {
                sh 'aws ecr get-login-password --region ap-southeast-1 --profile=ecr-user | docker login --username AWS --password-stdin 114992278129.dkr.ecr.ap-southeast-1.amazonaws.com'
            }
        }
        stage('Push Image') {
            steps {
                sh "docker push ${DOCKER_REGISTRY}:${TAG}"
                sh "docker push ${DOCKER_REGISTRY}:${TAG_LATEST}"
            }
        }
        stage('Delete Image') {
            steps {
                sh "docker rmi ${DOCKER_REGISTRY}:${TAG}"
                sh "docker rmi ${DOCKER_REGISTRY}:${TAG_LATEST}"
            }
        }
    }
    post {
        success {
            discordSend description: "Success: $env.GIT_COMMIT_MSG", footer: "hash: $GIT_COMMIT  by: $env.GIT_AUTHOR", link: env.BUILD_URL, result: currentBuild.currentResult, title: JOB_NAME, webhookURL: 'https://discord.com/api/webhooks/931203140865368104/tWFc49eeupS8-fA5t1LkZy9MNpn_gb2j9LNSN-CF7QHaBimBwD1l9pU3o5xlvhlWxRaK'
        }
        failure {
            discordSend notes:'@here', description: "Failed: $env.GIT_COMMIT_MSG", footer: "hash: $GIT_COMMIT  by: $env.GIT_AUTHOR", link: env.BUILD_URL, result: currentBuild.currentResult, title: JOB_NAME, webhookURL: 'https://discord.com/api/webhooks/931203140865368104/tWFc49eeupS8-fA5t1LkZy9MNpn_gb2j9LNSN-CF7QHaBimBwD1l9pU3o5xlvhlWxRaK'
        }
    }
}
