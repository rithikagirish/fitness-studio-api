import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from datetime import datetime, timedelta

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_signup_success(self):
        """Test successful user signup"""
        response = client.post("/signup", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        })
        assert response.status_code == 201
        assert response.json()["email"] == "john@example.com"
        assert response.json()["name"] == "John Doe"
    
    def test_signup_duplicate_email(self):
        """Test signup with duplicate email"""
        # First signup
        client.post("/signup", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        })
        
        # Duplicate signup
        response = client.post("/signup", json={
            "name": "Jane Doe",
            "email": "john@example.com",
            "password": "password456"
        })
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_login_success(self):
        """Test successful login"""
        # Signup first
        client.post("/signup", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        })
        
        # Login
        response = client.post("/login", json={
            "email": "john@example.com",
            "password": "password123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = client.post("/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

class TestClasses:
    """Test fitness class endpoints"""
    
    def get_auth_token(self):
        """Helper to get authentication token"""
        client.post("/signup", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        })
        response = client.post("/login", json={
            "email": "john@example.com",
            "password": "password123"
        })
        return response.json()["access_token"]
    
    def test_create_class_success(self):
        """Test creating a fitness class"""
        token = self.get_auth_token()
        future_date = (datetime.utcnow() + timedelta(days=7)).isoformat()
        
        response = client.post("/classes", 
            json={
                "name": "Yoga Flow",
                "dateTime": future_date,
                "instructor": "Jane Smith",
                "availableSlots": 20
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        assert response.json()["name"] == "Yoga Flow"
        assert response.json()["availableSlots"] == 20
    
    def test_create_class_unauthorized(self):
        """Test creating class without authentication"""
        future_date = (datetime.utcnow() + timedelta(days=7)).isoformat()
        
        response = client.post("/classes", json={
            "name": "Yoga Flow",
            "dateTime": future_date,
            "instructor": "Jane Smith",
            "availableSlots": 20
        })
        assert response.status_code == 403  # No authorization header
    
    def test_get_classes(self):
        """Test getting all classes"""
        token = self.get_auth_token()
        future_date = (datetime.utcnow() + timedelta(days=7)).isoformat()
        
        # Create a class first
        client.post("/classes", 
            json={
                "name": "Yoga Flow",
                "dateTime": future_date,
                "instructor": "Jane Smith",
                "availableSlots": 20
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Get all classes
        response = client.get("/classes")
        assert response.status_code == 200
        assert len(response.json()) >= 1

class TestBookings:
    """Test booking endpoints"""
    
    def setup_class_and_user(self):
        """Helper to setup user and class"""
        # Signup and login
        client.post("/signup", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        })
        login_response = client.post("/login", json={
            "email": "john@example.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        # Create a class
        future_date = (datetime.utcnow() + timedelta(days=7)).isoformat()
        class_response = client.post("/classes", 
            json={
                "name": "Yoga Flow",
                "dateTime": future_date,
                "instructor": "Jane Smith",
                "availableSlots": 5
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        class_id = class_response.json()["id"]
        
        return token, class_id
    
    def test_book_class_success(self):
        """Test successful booking"""
        token, class_id = self.setup_class_and_user()
        
        response = client.post("/book",
            json={
                "class_id": class_id,
                "client_name": "John Doe",
                "client_email": "john@example.com"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        assert response.json()["class_id"] == class_id
    
    def test_book_class_unauthorized(self):
        """Test booking without authentication"""
        response = client.post("/book", json={
            "class_id": 1,
            "client_name": "John Doe",
            "client_email": "john@example.com"
        })
        assert response.status_code == 403
    
    def test_book_nonexistent_class(self):
        """Test booking a non-existent class"""
        token, _ = self.setup_class_and_user()
        
        response = client.post("/book",
            json={
                "class_id": 9999,
                "client_name": "John Doe",
                "client_email": "john@example.com"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404
    
    def test_get_user_bookings(self):
        """Test getting user bookings"""
        token, class_id = self.setup_class_and_user()
        
        # Make a booking first
        client.post("/book",
            json={
                "class_id": class_id,
                "client_name": "John Doe",
                "client_email": "john@example.com"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Get bookings
        response = client.get("/bookings", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert len(response.json()) >= 1
