# 🏋️ ACEest Fitness & Gym – DevOps Project
---

## 📖 Table of Contents
- [Project Overview](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Conclusion](#-conclusion)

---
A complete **Flask-based Gym Management System** developed as part of a **DevOps assignment**, demonstrating modern software engineering practices including:

* Web application development using Flask
* Version control using Git & GitHub
* Automated testing using Pytest
* Containerization using Docker
* CI/CD pipelines using Jenkins and GitHub Actions

---

## 🚀 Project Overview

ACEest Fitness & Gym is a lightweight web application designed to manage:

* Client records
* Workout tracking
* Fitness program generation

The project showcases how an application evolves from **local development to a fully automated CI/CD pipeline**.

---

## 🧩 Features

### 🔐 Authentication

* Simple login system
* Default admin user:

  * Username: `admin`
  * Password: `admin`

### 👤 Client Management

* Add new clients
* View all clients
* Store membership status

### 🧠 Program Generation

* Automatically generate fitness programs
* Randomized based on predefined templates

### 🏋️ Workout Management

* Add workouts for clients
* View workout history
* Track duration and notes

### 🗄️ Database

* SQLite database (`aceest_fitness.db`)
* Automatically initialized

---

## 🏗️ Tech Stack

| Component        | Technology               |
| ---------------- | ------------------------ |
| Backend          | Flask (Python)           |
| Database         | SQLite                   |
| Testing          | Pytest                   |
| Containerization | Docker                   |
| CI/CD            | Jenkins + GitHub Actions |
| Version Control  | Git & GitHub             |

---

## 📁 Project Structure

```
aceest-fitness-gym/
│
├── app.py                  # Main Flask application
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
├── Dockerfile             # Docker configuration
├── Jenkinsfile            # Jenkins pipeline
├── .gitignore             # Ignored files
│
├── tests/
│   └── test_app.py        # Pytest test cases
│
└── .github/
    └── workflows/
        └── main.yml       # GitHub Actions workflow
```

---

## ⚙️ Local Setup & Execution

### 1️⃣ Clone the repository

```bash
git clone https://github.com/2024ht66055/ACEest-Fitness-Gym.git
cd ACEest-Fitness-Gym
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the application

```bash
python app.py
```

### 4️⃣ Open in browser

```
http://127.0.0.1:5000/
```

---

## 🧪 Running Tests (Pytest)

Run all tests using:

```bash
pytest
```

Tests include:

* Home route validation
* Database initialization
* Login functionality
* Error handling

---

## 🐳 Docker Setup

### Build Docker Image

```bash
docker build -t ACEest-Fitness-Gym .
```

### Run Container

```bash
docker run -p 5000:5000 ACEest-Fitness-Gym
```

### Run Tests Inside Docker

```bash
docker run --rm ACEest-Fitness-Gym pytest
```

---

## ⚙️ Jenkins Pipeline

The Jenkins pipeline automates the build process.

### Pipeline Stages:

1. **Checkout Code**

   * Pulls code from GitHub

2. **Build Docker Image**

   * Creates containerized environment

3. **Run Tests**

   * Executes Pytest inside Docker

### Outcome:

* Ensures code works in a clean environment
* Acts as a quality gate before deployment

---

## 🔄 GitHub Actions CI/CD

GitHub Actions automates testing on every code change.

### Trigger Conditions:

* On every `push`
* On every `pull_request`

### Workflow Steps:

1. Checkout repository
2. Setup Python environment
3. Install dependencies
4. Run Pytest
5. Build Docker image

### Result:

* Automatic validation of every change
* Prevents broken code from entering main branch

---

## 📸 Screenshots

Below Windows shows different activities done to complete the assignment.


**ACest-Fitness-Gym Testing Page**
*	Local setup and execution instructions.

<img width="903" height="488" alt="image" src="https://github.com/user-attachments/assets/6da60c72-8534-46ad-9151-94d298443260" />


<img width="416" height="362" alt="image" src="https://github.com/user-attachments/assets/716d6d4d-0b32-47b4-b94d-c4d3e0c89154" />

<img width="1003" height="370" alt="image" src="https://github.com/user-attachments/assets/8b9cbc79-1bef-4141-bef5-c8d85461f5a8" />

---

**GIT RESPOSITORY**


<img width="1128" height="586" alt="image" src="https://github.com/user-attachments/assets/7c22651c-0105-4c45-8f0d-f5e7a87727be" />
---
<img width="1334" height="469" alt="image" src="https://github.com/user-attachments/assets/bef4f0a7-d01e-4b45-aee6-3d954d851d16" />
---
<img width="1128" height="515" alt="image" src="https://github.com/user-attachments/assets/7b2199db-0e0f-47f6-aeaa-b62034b7c756" />
---

**JENKINS**

<img width="1348" height="454" alt="image" src="https://github.com/user-attachments/assets/a618f8c2-53f1-4899-beb3-826ec3a06910" />

<img width="1172" height="419" alt="image" src="https://github.com/user-attachments/assets/5ea63ed3-35a0-4f51-9bf8-9295c65bb0fe" />

<img width="1281" height="551" alt="image" src="https://github.com/user-attachments/assets/80f1d1e8-8e14-420e-a862-26059a24ff28" />

<img width="1011" height="292" alt="image" src="https://github.com/user-attachments/assets/c8f5a0f4-d2b0-4062-b74f-b65e193f8cfc" />

<img width="1280" height="516" alt="image" src="https://github.com/user-attachments/assets/2f8033ae-ca1a-44c6-be4e-9560909f94c5" />

<img width="1172" height="508" alt="image" src="https://github.com/user-attachments/assets/168b3258-0a57-4724-94b1-cbe7e7b3ad55" />

<img width="1011" height="292" alt="image" src="https://github.com/user-attachments/assets/89634ad1-5c20-43c6-86e6-9145fe71a41d" />

```
---

## 🔁 DevOps Workflow Summary

```
Developer Code → GitHub → GitHub Actions (Test + Build)
                    ↓
                 Jenkins (Build + Test in Docker)
                    ↓
               Verified Application
```
```
---


## 📌 Key DevOps Concepts Demonstrated

* Version Control with Git
* Continuous Integration (CI)
* Automated Testing
* Containerization (Docker)
* Pipeline Automation (Jenkins & GitHub Actions)
* Environment Consistency

---

## ⚠️ Notes

* SQLite database is created locally on first run
* Database file is excluded using `.gitignore`
* Docker container uses an isolated environment
* No production deployment included (development-focused project)

---

## 👨‍💻 Author

* Rupesh Naik - 2024HT66055
* Developed as part of a DevOps learning assignment.

---

## 🎯 Conclusion

This project demonstrates how a simple Python application can be transformed into a **production-ready, automated pipeline-driven system** using modern DevOps tools.

It ensures:

* Code reliability
* Faster development cycles
* Automated validation
* Environment consistency

---
