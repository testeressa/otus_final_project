# otus_final_project
https://github.com/OtusTeam/QA-Python/blob/master/project/hw.md

# Дополнительные шаги по настройке Jenkins агента
https://www.jenkins.io/doc/book/using/using-agents/

Cгенерировать публичный и приватный ключ, 
добавить их в директорию jenkins_agent в файлы
jenkins_agent_key и jenkins_agent_key.pub;
значение из jenkins_agent_key.pub продублировать в файл 
authorized_keys

# запуск контейнеров проекта
LOCAL_IP=192.168.0.21 OPENCART_PORT=8090 PHPADMIN_PORT=8092 docker compose up -d
ip из ifconfig en0 и LOCAL_IP должны совпадать

# команда запуска jenkins
docker run -p 8080:8080 jenkins/jenkins:lts

# команда запуска jenkins_agent
docker run -d --name=agent1 -p 22:22 \                                                  
-e "JENKINS_AGENT_SSH_PUBKEY=jenkins_agent_key.pub" \
jenkins_agent_pytest:latest

