FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl  \
    openssh-server \
    openjdk-17-jdk \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin without-password/' /etc/ssh/sshd_config
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/usr/sbin/sshd", "-D"]