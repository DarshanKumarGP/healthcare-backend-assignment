# Healthcare Backend API

A secure healthcare backend application built using **Django**, **Django REST Framework**, **PostgreSQL**, and **JWT Authentication**.

This project was developed as part of the WhatBytes Backend Developer Internship assignment.

---

## Features

* Custom email-based authentication
* JWT authentication using Simple JWT
* User registration and login
* Patient management APIs
* Doctor management APIs
* Patient-doctor assignment APIs
* PostgreSQL database integration
* Environment-based configuration
* Global exception handling
* Input validation and permissions
* Pagination support
* Postman collection included

---

## Tech Stack

* Python 3.x
* Django
* Django REST Framework
* PostgreSQL
* Simple JWT
* Python Decouple
* Django CORS Headers

---

## Project Structure

```text
healthcare-backend-assignment/
│
├── accounts/
├── core/
├── doctors/
├── mappings/
├── patients/
├── healthcare_backend/
├── postman_collection.json
├── requirements.txt
├── .env.example
├── manage.py
└── README.md
```

---

## Setup Instructions

### Clone Repository

```bash
git clone <repository-url>
cd healthcare-backend-assignment
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Configuration

Create a PostgreSQL database:

```sql
CREATE DATABASE healthcare_db;
```

Create a `.env` file using `.env.example`.

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=1
```

---

## Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Run Development Server

```bash
python manage.py runserver
```

Server:

```text
http://127.0.0.1:8000/
```

---

## Authentication APIs

| Method | Endpoint              |
| ------ | --------------------- |
| POST   | `/api/auth/register/` |
| POST   | `/api/auth/login/`    |

---

## Patient APIs

| Method | Endpoint              |
| ------ | --------------------- |
| POST   | `/api/patients/`      |
| GET    | `/api/patients/`      |
| GET    | `/api/patients/<id>/` |
| PUT    | `/api/patients/<id>/` |
| DELETE | `/api/patients/<id>/` |

---

## Doctor APIs

| Method | Endpoint             |
| ------ | -------------------- |
| POST   | `/api/doctors/`      |
| GET    | `/api/doctors/`      |
| GET    | `/api/doctors/<id>/` |
| PUT    | `/api/doctors/<id>/` |
| DELETE | `/api/doctors/<id>/` |

---

## Patient-Doctor Mapping APIs

| Method | Endpoint                      |
| ------ | ----------------------------- |
| POST   | `/api/mappings/`              |
| GET    | `/api/mappings/`              |
| GET    | `/api/mappings/<patient_id>/` |
| DELETE | `/api/mappings/<id>/`         |

---

## Authentication

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

JWT tokens are generated using Simple JWT.

---

## API Response Format

Success Response:

```json
{
    "success": true,
    "message": "Request successful.",
    "data": {}
}
```

Error Response:

```json
{
    "success": false,
    "message": "Request failed.",
    "errors": {}
}
```

---

## Postman Collection

The repository includes:

```text
postman_collection.json
```

Import the collection into Postman to test all APIs.

---

## Environment Variables

Sensitive values are managed using environment variables.

The `.env` file is excluded from version control.

---

## Author

Darshan Kumar

Backend Developer Internship Assignment
WhatBytes
