# IS218 Module 14 - FastAPI Calculator with JWT Authentication and BREAD Operations

## Overview

This project is the Module 14 assignment for IS218. It extends the Module 13 JWT Authentication project by implementing complete BREAD (Browse, Read, Edit, Add, Delete) functionality for user calculations.

Users can securely register and log in using JWT authentication, then create, browse, edit, view, and delete their own calculations through both the API and frontend.

---

# Features

## Authentication

- User Registration
- User Login
- Password hashing using bcrypt
- JWT Access Token generation
- JWT token validation
- Duplicate username/email validation
- Protected calculation endpoints

---

## Calculation BREAD Operations

### Browse

- View all calculations belonging to the authenticated user

### Read

- View a single calculation by ID

### Add

- Create new calculations
- Supported operations:
  - Add
  - Subtract
  - Multiply
  - Divide

### Edit

- Update operands or operation type
- Automatically recalculates the result

### Delete

- Delete calculations belonging to the logged-in user

---

## Frontend

- Home page
- Registration page
- Login page
- Calculator page
- Client-side validation
- JWT stored in Local Storage
- Authenticated calculation management

---

## Security

- Password hashing using bcrypt
- JWT authentication
- User ownership verification
- Protected calculation routes
- Invalid login handling
- Duplicate account protection

---

## Testing

- Unit Tests
- Integration Tests
- Playwright End-to-End Tests
- Coverage Reports

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
- Docker
- Docker Compose
- Playwright
- Pytest
- GitHub Actions

---

# Project Structure

```
IS218-Module14/

├── app/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── operations/
│   ├── security.py
│   └── database.py
│
├── static/
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
git clone git@github.com:davidcruzzy03/IS218-Module14.git
```

Enter the project

```bash
cd IS218-Module14
```

Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it

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

Build the application

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

Generate coverage

```bash
pytest --cov=app --cov=main
```

Current Results

```
68+ Tests Passing

90%+ Coverage
```

---

# Authentication Flow

1. Register a new account
2. Password is securely hashed
3. Login using username and password
4. JWT access token is created
5. JWT stored in browser Local Storage
6. Authenticated requests include the token
7. Users may only access their own calculations

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
| GET | /calculations/{id} | Read one calculation |
| POST | /calculations | Add calculation |
| PUT | /calculations/{id} | Edit calculation |
| DELETE | /calculations/{id} | Delete calculation |

---

# Continuous Integration

GitHub Actions automatically:

- Runs Unit Tests
- Runs Integration Tests
- Runs Playwright Tests
- Generates Coverage Reports
- Builds Docker Image
- Runs Security Scan
- Pushes Docker Image to Docker Hub

---

# Docker Hub

Docker Hub Repository

```
https://hub.docker.com/r/davidcruzzy03/is218-module14
```

---

# GitHub Repository

```
https://github.com/davidcruzzy03/IS218-Module14
```

---

# Learning Outcomes

This module expanded my understanding of:

- JWT Authentication
- User Authorization
- Secure Password Storage
- RESTful API Design
- BREAD Operations
- User Ownership Verification
- Playwright End-to-End Testing
- Docker Deployment
- GitHub Actions CI/CD
- Secure Full-Stack Development

---

# Author

**David Cruz**

IS218 – Web Systems Development

GitHub

https://github.com/davidcruzzy03