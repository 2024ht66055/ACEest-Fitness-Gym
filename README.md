# 🏋️ ACEest Fitness & Gym – DevOps Project

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
git clone https://github.com/your-username/aceest-fitness-gym.git
cd aceest-fitness-gym
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
docker build -t aceest-gym .
```

### Run Container

```bash
docker run -p 5000:5000 aceest-gym
```

### Run Tests Inside Docker

```bash
docker run --rm aceest-gym pytest
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

## 🔁 DevOps Workflow Summary

```
Developer Code → GitHub → GitHub Actions (Test + Build)
                    ↓
                 Jenkins (Build + Test in Docker)
                    ↓
               Verified Application
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
