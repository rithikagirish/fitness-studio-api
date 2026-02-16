from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta, datetime
import logging

from app.database import get_db, init_db, User, FitnessClass, Booking
from app.schemas import (
    UserSignup, UserLogin, UserResponse, Token,
    ClassCreate, ClassResponse,
    BookingCreate, BookingResponse
)
from app.auth import (
    get_password_hash, authenticate_user, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.utils import convert_to_ist, get_current_ist_time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Fitness Studio API",
    description="API for managing fitness classes and bookings",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    logger.info("Database initialized")

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to Fitness Studio API",
        "docs": "/docs",
        "version": "1.0.0"
    }

# Authentication Endpoints
@app.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **name**: User's full name
    - **email**: User's email (must be unique)
    - **password**: Password (minimum 6 characters)
    """
    logger.info(f"Signup attempt for email: {user_data.email}")
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        logger.warning(f"Signup failed: Email already registered - {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"User created successfully: {user_data.email}")
    return new_user

@app.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return access token
    
    - **email**: User's email
    - **password**: User's password
    """
    logger.info(f"Login attempt for email: {user_credentials.email}")
    
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        logger.warning(f"Login failed: Invalid credentials - {user_credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    logger.info(f"Login successful: {user_credentials.email}")
    return {"access_token": access_token, "token_type": "bearer"}

# Class Endpoints
@app.post("/classes", response_model=ClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(
    class_data: ClassCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new fitness class (requires authentication)
    
    - **name**: Name of the class (e.g., "Yoga Flow")
    - **dateTime**: Date and time in ISO format (stored in IST)
    - **instructor**: Name of the instructor
    - **availableSlots**: Number of available slots
    """
    logger.info(f"Creating class: {class_data.name} by user: {current_user.email}")
    
    # Validate that class is in the future
    ist_time = convert_to_ist(class_data.dateTime)
    current_ist = get_current_ist_time()
    
    if ist_time < current_ist:
        logger.warning(f"Class creation failed: Past date/time")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create class in the past"
        )
    
    new_class = FitnessClass(
        name=class_data.name,
        dateTime=class_data.dateTime,
        instructor=class_data.instructor,
        availableSlots=class_data.availableSlots,
        created_by=current_user.id
    )
    
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    
    logger.info(f"Class created successfully: {new_class.id}")
    return new_class

@app.get("/classes", response_model=List[ClassResponse])
def get_classes(db: Session = Depends(get_db)):
    """
    Fetch all upcoming fitness classes
    
    Returns classes scheduled from now onwards, ordered by date/time
    """
    logger.info("Fetching all upcoming classes")
    
    current_time = datetime.utcnow()
    classes = db.query(FitnessClass)\
        .filter(FitnessClass.dateTime >= current_time)\
        .order_by(FitnessClass.dateTime)\
        .all()
    
    logger.info(f"Found {len(classes)} upcoming classes")
    return classes

# Booking Endpoints
@app.post("/book", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def book_class(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Book a slot in a fitness class (requires authentication)
    
    - **class_id**: ID of the class to book
    - **client_name**: Name of the person booking
    - **client_email**: Email of the person booking
    """
    logger.info(f"Booking attempt for class {booking_data.class_id} by user: {current_user.email}")
    
    # Get the class
    fitness_class = db.query(FitnessClass).filter(
        FitnessClass.id == booking_data.class_id
    ).first()
    
    if not fitness_class:
        logger.warning(f"Booking failed: Class not found - {booking_data.class_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    # Check if class is in the future
    if fitness_class.dateTime < datetime.utcnow():
        logger.warning(f"Booking failed: Class already passed - {booking_data.class_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot book a class that has already passed"
        )
    
    # Check if user already booked this class
    existing_booking = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.class_id == booking_data.class_id
    ).first()
    
    if existing_booking:
        logger.warning(f"Booking failed: Already booked - {booking_data.class_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already booked this class"
        )
    
    # Check available slots
    if fitness_class.availableSlots <= 0:
        logger.warning(f"Booking failed: No slots available - {booking_data.class_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No available slots for this class"
        )
    
    # Create booking
    new_booking = Booking(
        user_id=current_user.id,
        class_id=booking_data.class_id,
        client_name=booking_data.client_name,
        client_email=booking_data.client_email
    )
    
    # Decrease available slots
    fitness_class.availableSlots -= 1
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    logger.info(f"Booking successful: {new_booking.id}")
    return new_booking

@app.get("/bookings", response_model=List[BookingResponse])
def get_user_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    View all bookings by the authenticated user
    
    Returns all bookings made by the current user, ordered by booking date
    """
    logger.info(f"Fetching bookings for user: {current_user.email}")
    
    bookings = db.query(Booking)\
        .filter(Booking.user_id == current_user.id)\
        .order_by(Booking.booked_at.desc())\
        .all()
    
    logger.info(f"Found {len(bookings)} bookings for user: {current_user.email}")
    return bookings
