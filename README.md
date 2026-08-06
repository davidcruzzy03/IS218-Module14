# IS218 Final Project - FastAPI Calculator with JWT Authentication, BREAD Operations, and Report Dashboard

## Overview

This project is the Final Project for IS218 Web Systems Development.

It extends the previous FastAPI Calculator by implementing secure JWT authentication, complete BREAD (Browse, Read, Edit, Add, Delete) operations for calculations, and a new authenticated Report Dashboard.

Users can:

- Register and log in securely
- Perform calculator operations
- Browse, read, edit, add, and delete their calculations
- View personalized reports and statistics
- Filter calculation history
- Clear calculation history

The application includes automated unit, integration, and Playwright end-to-end testing, Docker deployment, PostgreSQL integration, and GitHub Actions CI/CD.

---

# Features

## Authentication

- User Registration
- User Login
- Password hashing using bcrypt
- JWT Access Token generation
- JWT validation
- Duplicate username/email validation
- Protected API endpoints
- User ownership verification

---

## Calculation Management (BREAD)

### Browse

- View all calculations belonging to the authenticated user

### Read

- View a single saved calculation

### Add

Create calculations using:

- Add
- Subtract
- Multiply
- Divide

### Edit

- Update operands
- Update operation type
- Automatically recalculate results

### Delete

- Delete calculations belonging to the logged-in user

---

## Report Dashboard

Authenticated users can access a dashboard that displays:

- Total calculations
- Average first operand
- Average second operand
- Most frequently used operation
- Operation counts
- Complete calculation history
- Filter history by operation
- Clear calculation history

All reports are user-specific and protected using JWT authentication.

---

## Frontend

- Home page
- Register page
- Login page
- Calculator page
- Report Dashboard
- Client-side validation
- JWT stored in browser Local Storage
- History filtering
- History clearing

---

## Security

- Password hashing with bcrypt
- JWT Authentication
- Protected routes
- User ownership verification
- Input validation
- Duplicate account protection

---

## Testing

- Unit Tests
- Integration Tests
- Playwright End-to-End Tests
- Report Dashboard Tests
- Coverage Reports

### Final Results

- **85 Tests Passed**
- **92% Code Coverage**

---

## DevOps

- Docker
- Docker Compose
- PostgreSQL
- pgAdmin
- GitHub Actions
- Docker Hub Deployment

---

# Technologies Used

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Passlib (bcrypt)
- python-jose (JWT)
- HTML
- CSS
- JavaScript
- Playwright
- Pytest
- Docker
- Docker Compose
- GitHub Actions

---

# Project Structure

```text
IS218-Module14/

├── app/
│   ├── core/
│   ├── models/
│   ├── operations/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   └── security.py
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── .github/
│   └── workflows/
│
├── Dockerfile
├── docker-compose.yml
├── main.py
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/davidcruzzy03/IS218-Module14.git
```

Enter the project

```bash
cd IS218-Module14
```

Create a virtual environment

```bash
python3 -m venv .venv
```

Activate the environment

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/calculator_db

TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/calculator_test_db

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Running with Docker

Build and start the application

```bash
docker compose up -d --build
```

Stop the application

```bash
docker compose down
```

---

# Running the Application

Run locally

```bash
uvicorn main:app --reload
```

Application

```
http://localhost:8000
```

Register

```
http://localhost:8000/register
```

Login

```
http://localhost:8000/login
```

Report Dashboard

```
http://localhost:8000/dashboard
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

# Running Tests

Run all tests

```bash
python -m pytest -v
```

Run unit tests

```bash
python -m pytest tests/unit -v
```

Run integration tests

```bash
python -m pytest tests/integration -v
```

Run Playwright tests

```bash
python -m pytest tests/e2e -v
```

Run coverage

```bash
python -m pytest \
tests/unit \
tests/integration \
tests/e2e \
--cov=app \
--cov-report=term-missing
```

---

# API Endpoints

## User Routes

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /users/register | Register a user |
| POST | /users/login | Login user |

---

## Calculation Routes

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /calculations | Browse calculations |
| GET | /calculations/{id} | Read calculation |
| POST | /calculations | Add calculation |
| PUT | /calculations/{id} | Edit calculation |
| DELETE | /calculations/{id} | Delete calculation |

---

## Report Routes

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /reports/history | View user calculation history |
| GET | /reports/summary | View calculation statistics |
| DELETE | /reports/history | Clear user calculation history |

---

# Continuous Integration

GitHub Actions automatically:

- Runs Unit Tests
- Runs Integration Tests
- Runs Playwright E2E Tests
- Generates Coverage Reports
- Builds Docker Image
- Runs Security Scan
- Pushes Docker Image to Docker Hub

---

# Docker Hub

https://hub.docker.com/r/davidcruzzy03/is218-module14

---

# GitHub Repository

https://github.com/davidcruzzy03/IS218-Module14

---

# Learning Outcomes

This project strengthened my understanding of:

- JWT Authentication
- Password Hashing
- User Authorization
- REST API Development
- FastAPI
- SQLAlchemy
- PostgreSQL
- BREAD Operations
- Report Dashboard Development
- Playwright End-to-End Testing
- Docker
- GitHub Actions CI/CD
- Secure Full-Stack Development

---

# Author

**David Cruz**

IS218 – Web Systems Development

GitHub:

https://github.com/davidcruzzy03