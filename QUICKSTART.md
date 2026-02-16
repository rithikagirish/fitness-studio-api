# 🚀 Quick Start Guide - Fitness Studio API

Get the API up and running in 5 minutes!

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Navigate to project directory
```bash
cd fitness-studio-api
```

### 2. Create and activate virtual environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application

**Option A: Using uvicorn directly**
```bash
uvicorn app.main:app --reload
```

**Option B: Using the run script**
```bash
python run.py
```

### 5. Test the API

Open your browser and go to:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Root Endpoint**: http://localhost:8000

## Testing the API (5-Minute Flow)

### Step 1: Sign Up (Create Account)
```bash
curl -X POST "http://localhost:8000/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Step 2: Login (Get Token)
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Copy the `access_token` from the response!**

### Step 3: Create a Class
```bash
curl -X POST "http://localhost:8000/classes" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Morning Yoga",
    "dateTime": "2025-06-15T10:00:00Z",
    "instructor": "Jane Smith",
    "availableSlots": 20
  }'
```

### Step 4: View All Classes
```bash
curl -X GET "http://localhost:8000/classes"
```

### Step 5: Book a Class
```bash
curl -X POST "http://localhost:8000/book" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "John Doe",
    "client_email": "john@example.com"
  }'
```

### Step 6: View Your Bookings
```bash
curl -X GET "http://localhost:8000/bookings" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Using Swagger UI (Easiest Way!)

1. Go to http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"

For authenticated endpoints:
1. First call `/login` to get a token
2. Click the "Authorize" button (🔒) at the top
3. Enter: `Bearer YOUR_TOKEN_HERE`
4. Click "Authorize"
5. Now you can call protected endpoints!

## Using Postman

1. Import the `Fitness_Studio_API.postman_collection.json` file
2. Set the base_url variable to `http://localhost:8000`
3. Run the requests in order:
   - Sign Up
   - Login (automatically saves token)
   - Create Class
   - Book Class
   - Get Bookings

## Running Tests

```bash
pytest tests/ -v
```

For coverage report:
```bash
pytest tests/ --cov=app --cov-report=html
```

View coverage report at: `htmlcov/index.html`

## Troubleshooting

### Port already in use?
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### Database issues?
```bash
# Delete the database and restart
rm fitness_studio.db
python run.py
```

### Import errors?
Make sure your virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

## What's Next?

- Explore the full [README.md](README.md) for detailed documentation
- Check out the [API Documentation](http://localhost:8000/docs)
- Run the tests to understand the codebase
- Customize the SECRET_KEY in `app/auth.py` for production
- Consider switching to PostgreSQL for production use

## Need Help?

- Check the detailed README.md
- Look at the test files for usage examples
- Use the Swagger UI for interactive testing
- Review the code comments in each module

Happy coding! 🎉
