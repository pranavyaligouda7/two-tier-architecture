#!/bin/bash

apt update -y

apt install -y docker.io docker-compose-v2 git

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

cd /home/ubuntu

git clone https://github.com/pranavyaligouda7/two-tier-architecture.git

cd two-tier-architecture

cat > .env <<EOF
MYSQL_ROOT_PASSWORD=root123
MYSQL_DATABASE=twotier
MYSQL_USER=pranav
MYSQL_PASSWORD=password123
EOF

docker compose up -d