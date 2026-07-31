# IS218 Module 13 - JWT Authentication FastAPI Calculator

## Overview

This project is the Module 13 assignment for IS218. It extends the FastAPI Calculator application by implementing secure user authentication using JSON Web Tokens (JWT), frontend login and registration pages, and automated end-to-end testing with Playwright.

The application allows users to register, log in, perform calculator operations, and securely authenticate using JWT tokens.

---

## Features

### Authentication

- User registration
- User login
- Password hashing using bcrypt
- JWT access token generation
- JWT token validation
- Duplicate email and username validation
- Invalid credential handling

### Calculator

- Addition
- Subtraction
- Multiplication
- Division
- Division-by-zero validation
- Calculation history stored in PostgreSQL

### Frontend

- Home page
- Register page
- Login page
- Client-side form validation
- Stores JWT token in browser Local Storage after successful login

### Testing

- Unit Tests
- Integration Tests
- Playwright End-to-End Tests
- Pytest Coverage Report

### DevOps

- Docker Compose
- PostgreSQL
- pgAdmin
- GitHub Actions CI
- Docker Hub Integration

---

## Technologies Used

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Passlib (bcrypt)
- python-jose (JWT)
- Jinja2
- HTML
- CSS
- JavaScript
- Docker
- Docker Compose
- Pytest
- Playwright
- GitHub Actions

---

## Project Structure

```
IS218-Module13/
│
├── app/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── security.py
│   ├── database.py
│   └── operations/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── index.html
│   ├── register.html
│   └── login.html
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── Dockerfile
├── docker-compose.yml
├── main.py
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/davidcruzzy03/IS218-Module13.git
```

Navigate into the project

```bash
cd IS218-Module13
```

Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it

Linux / macOS

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

## Environment Variables

Create a `.env` file.

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/calculator_db
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/calculator_test_db

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Running with Docker

Build the project

```bash
docker compose up -d --build
```

Stop containers

```bash
docker compose down
```

---

## Running the Application

Start the FastAPI server

```bash
uvicorn main:app --reload
```

Open:

```
http://localhost:8000
```

Registration page

```
http://localhost:8000/register
```

Login page

```
http://localhost:8000/login
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

## Running Tests

Run all tests

```bash
pytest -v
```

Run unit tests

```bash
pytest tests/unit
```

Run integration tests

```bash
pytest tests/integration
```

Run Playwright tests

```bash
pytest tests/e2e
```

Generate coverage report

```bash
pytest --cov=app --cov=main
```

Current Results

```
68 tests passed
93% coverage
```

---

## Authentication Flow

1. User registers with username, email, and password.
2. Password is securely hashed using bcrypt.
3. User logs in with valid credentials.
4. A JWT access token is generated.
5. The frontend stores the token in Local Storage.
6. Future authenticated requests can use the JWT token.

---

## API Endpoints

### User Routes

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/users/register` | Register a new user |
| POST | `/users/login` | Authenticate user |

### Calculator Routes

| Method | Endpoint |
|---------|----------|
| GET | `/calculations` |
| GET | `/calculations/{id}` |
| POST | `/calculations` |
| PUT | `/calculations/{id}` |
| DELETE | `/calculations/{id}` |

---

## Continuous Integration

This project uses GitHub Actions to automatically:

- Run unit tests
- Run integration tests
- Run Playwright tests
- Generate coverage reports
- Build the Docker image
- Push the image to Docker Hub

---

## Learning Outcomes

Through this module I learned how to:

- Implement JWT authentication
- Secure user passwords with bcrypt hashing
- Build login and registration pages
- Validate user input on both the client and server
- Write end-to-end tests using Playwright
- Integrate automated testing into a CI/CD workflow
- Deploy containerized applications using Docker

---

## Author

**David Cruz**

IS218 – Web Systems Development

GitHub: https://github.com/davidcruzzy03