pipeline {
    agent any

    options {
        timestamps()
        ansiColor('xterm')
    }

    environment {
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        PYTHONDONTWRITEBYTECODE = '1'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Backend') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    python3 -m pip install poetry
                    poetry install
                '''
            }
        }

        stage('Validate Workflows') {
            steps {
                sh 'poetry run validate-workflows'
            }
        }

        stage('Backend Tests') {
            steps {
                sh '''
                    export PYTHONPATH=backend
                    poetry run pytest backend/tests/test_main.py backend/tests/test_metadata.py backend/tests/test_roadmap.py
                '''
            }
        }

        stage('Setup Frontend') {
            steps {
                dir('frontend') {
                    sh 'npm ci'
                }
            }
        }

        stage('Frontend Lint') {
            steps {
                dir('frontend') {
                    sh 'npm run lint'
                }
            }
        }
    }
}
