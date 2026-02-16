# Fitness Studio API 🏋️‍♀️

A RESTful API built with FastAPI for managing fitness studio classes and bookings.

## Features ✨

- **User Authentication**: JWT-based authentication with signup and login
- **Class Management**: Create and view fitness classes
- **Booking System**: Book classes with slot management and overbooking prevention
- **Timezone Support**: All times stored and managed in IST (Indian Standard Time)
- **Comprehensive Validation**: Request validation and error handling
- **API Documentation**: Auto-generated Swagger/OpenAPI docs
- **Unit Tests**: Comprehensive test coverage with pytest

## Tech Stack 🛠️

- **Language**: Python 3.8+
- **Framework**: FastAPI
- **Database**: SQLite (can be easily switched to PostgreSQL/MongoDB)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens) with python-jose
- **Password Hashing**: bcrypt via passlib
- **Testing**: pytest
- **Timezone**: pytz for IST management

## Project Structure 📁

```
fitness-studio-api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application and endpoints
│   ├── database.py       # Database models and configuration
│   ├── schemas.py        # Pydantic schemas for validation
│   ├── auth.py           # Authentication utilities
│   └── utils.py          # Timezone utilities
├── tests/
│   ├── __init__.py
│   └── test_api.py       # Unit tests
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Installation & Setup 🚀

### 1. Clone the repository

```bash
git clone <repository-url>
cd fitness-studio-api
```

### 2. Create virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

### 5. (Optional) Populate with Sample Data

To quickly test the API with sample data:

```bash
python seed_data.py
```

This creates:
- **4 sample users** (alice@example.com, bob@example.com, charlie@example.com, diana@example.com)
- **8 fitness classes** (Yoga, HIIT, Zumba, Pilates, Spin, CrossFit, Meditation)
- **7 sample bookings**

All sample users have the password: `password123`

### 6. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints 📡

### Authentication

#### Sign Up
```http
POST /signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-02-16T10:00:00"
}
```

#### Log In
```http
POST /login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Classes

#### Create Class (Requires Authentication)
```http
POST /classes
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Yoga Flow",
  "dateTime": "2025-06-15T10:00:00Z",
  "instructor": "John Doe",
  "availableSlots": 20
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Yoga Flow",
  "dateTime": "2025-06-15T10:00:00",
  "instructor": "John Doe",
  "availableSlots": 20
}
```

#### Get All Classes
```http
GET /classes
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "HIIT Session",
    "dateTime": "2025-06-18T08:00:00",
    "instructor": "Jane Smith",
    "availableSlots": 10
  }
]
```

### Bookings

#### Book a Class (Requires Authentication)
```http
POST /book
Authorization: Bearer <token>
Content-Type: application/json

{
  "class_id": 1,
  "client_name": "Alice",
  "client_email": "alice@example.com"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "class_id": 1,
  "client_name": "Alice",
  "client_email": "alice@example.com",
  "booked_at": "2025-02-16T10:30:00",
  "fitness_class": {
    "id": 1,
    "name": "Yoga Flow",
    "dateTime": "2025-06-15T10:00:00",
    "instructor": "John Doe",
    "availableSlots": 19
  }
}
```

#### Get User Bookings (Requires Authentication)
```http
GET /bookings
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "class_id": 1,
    "client_name": "Alice",
    "client_email": "alice@example.com",
    "booked_at": "2025-02-16T10:30:00",
    "fitness_class": {
      "id": 1,
      "name": "Yoga Flow",
      "dateTime": "2025-06-15T10:00:00",
      "instructor": "John Doe",
      "availableSlots": 19
    }
  }
]
```

## Authentication Flow 🔐

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

1. **Sign up** with `/signup` endpoint
2. **Log in** with `/login` to receive an access token
3. **Use the token** in the Authorization header for protected endpoints
4. **Token expires** after 60 minutes (configurable)

## Running Tests 🧪

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=app --cov-report=html
```

## Key Features Implementation 🎯

### 1. Authentication
- ✅ JWT-based token authentication
- ✅ Password hashing with bcrypt
- ✅ Token expiration (60 minutes default)
- ✅ Protected endpoints

### 2. Validation & Error Handling
- ✅ Pydantic schema validation
- ✅ Email format validation
- ✅ Minimum password length (6 characters)
- ✅ Future date validation for classes
- ✅ Slot availability checking
- ✅ Duplicate booking prevention

### 3. Business Logic
- ✅ Automatic slot deduction on booking
- ✅ Overbooking prevention
- ✅ Past class booking prevention
- ✅ User can't book same class twice

### 4. Timezone Management
- ✅ All times stored in IST
- ✅ Timezone conversion utilities
- ✅ Current time checks in IST

### 5. Logging
- ✅ Request logging
- ✅ Authentication attempts
- ✅ Error logging
- ✅ Business operation logging

## Configuration ⚙️

### Database
The application uses SQLite by default. To change to PostgreSQL or another database:

1. Update `SQLALCHEMY_DATABASE_URL` in `app/database.py`
2. Install appropriate database driver
3. Update connection string

Example for PostgreSQL:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

### JWT Secret Key
⚠️ **Important**: Change the secret key in production!

Update in `app/auth.py`:
```python
SECRET_KEY = "your-production-secret-key"
```

### Token Expiration
Default: 60 minutes

Update in `app/auth.py`:
```python
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Change as needed
```

## Error Codes & Responses 📋

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error, business logic violation) |
| 401 | Unauthorized (invalid credentials) |
| 403 | Forbidden (missing/invalid token) |
| 404 | Not Found |
| 422 | Unprocessable Entity (validation error) |
| 500 | Internal Server Error |

## Sample Data 📊

The project includes sample data to help you get started quickly:

### Automated Seeding

Run the seed script to populate your database:

```bash
python seed_data.py
```

**What gets created:**
- 4 users (Alice, Bob, Charlie, Diana)
- 8 fitness classes (various types and times)
- 7 bookings across different classes

**Test Credentials:**
```
Email: alice@example.com   | Password: password123
Email: bob@example.com     | Password: password123
Email: charlie@example.com | Password: password123
Email: diana@example.com   | Password: password123
```

### Manual Sample Data

See `sample_data.json` for the complete sample dataset structure. You can use this as a reference for API requests.

## Example Usage with cURL 💻

### Sign Up
```bash
curl -X POST "http://localhost:8000/signup" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'
```

### Create Class
```bash
curl -X POST "http://localhost:8000/classes" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Yoga","dateTime":"2025-06-15T10:00:00Z","instructor":"Jane","availableSlots":20}'
```

### Book Class
```bash
curl -X POST "http://localhost:8000/book" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"class_id":1,"client_name":"Alice","client_email":"alice@example.com"}'
```

## Future Enhancements 🚀

- [ ] Email verification
- [ ] Password reset functionality
- [ ] Class cancellation
- [ ] Booking cancellation with refund policy
- [ ] Admin role for class management
- [ ] Waitlist functionality
- [ ] Class capacity alerts
- [ ] Email notifications
- [ ] Payment integration
- [ ] Class ratings and reviews

## License 📄

This project is created for educational purposes as part of a Backend Developer Intern Assignment.

## Contact 📧

For questions or feedback, please reach out through the repository issues.
