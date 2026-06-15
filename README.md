# 🚀 Two-Tier Flask Web Application (DevOps CI/CD on Single EC2)

A complete **production-style DevOps project** demonstrating:

- Flask Web Application (Backend)
- MySQL Database (Containerized)
- Jenkins CI/CD Pipeline
- Docker + Docker Compose
- AWS EC2 Ubuntu (Single Machine Hosting)
- Automated Deployment + Health Checks

---

# 🧠 Project Architecture

## 🏗️ Single EC2 Deployment Architecture

👉 Everything runs on ONE AWS EC2 Ubuntu machine:

- Jenkins (CI/CD Server)
- Docker Engine
- Flask Application Container
- MySQL Container

---

## 🔥 SYSTEM ARCHITECTURE DIAGRAM

```mermaid
flowchart TB

Developer --> GitHub

GitHub --> Jenkins

subgraph AWS EC2 Ubuntu Server
    Jenkins --> DockerCompose
    DockerCompose --> FlaskContainer
    DockerCompose --> MySQLContainer
end

FlaskContainer --> MySQLContainer
FlaskContainer --> UserBrowser
