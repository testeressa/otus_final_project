pipeline {
    agent { label 'agent1' }

    environment {
        REPO_URL = 'https://github.com/testeressa/otus_final_project.git'
        ALLURE_RESULTS = './allure-results'
    }

    parameters {
        string(name: 'SELENOID_URL', defaultValue: 'http://host.docker.internal:4444/wd/hub', description: 'Selenoid Executor URL')
        string(name: 'OPENCART_URL', defaultValue: 'http://192.168.65.254:8090', description: 'OpenCart App URL')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Browser')
        string(name: 'BROWSER_VERSION', defaultValue: '128.0', description: 'Browser Version')
        choice(name: 'THREADS', choices: ['1', '2', '4'], description: 'Number of Threads')
    }

    stages {
        stage('Checkout') {
            steps {
                    git url: "${REPO_URL}", branch: 'main'
                }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    pytest ${WORKSPACE}/src/tests/ \
                        --alluredir=${ALLURE_RESULTS} \
                        --browser ${BROWSER} \
                        --browser_version ${BROWSER_VERSION} \
                        --headless \
                        --selenoid \
                        --selenoid_url ${SELENOID_URL} \
                        --url ${OPENCART_URL}
                '''
            }
        }
    }

    post {
        always {
            script {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    allure includeProperties: false, jdk: '', results: [[path: "/allure-results"]]
                }
            }
            archiveArtifacts artifacts: "/allure-results/**", fingerprint: true, allowEmptyArchive: true
        }
    }
}