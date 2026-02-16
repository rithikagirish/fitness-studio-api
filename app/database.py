from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    bookings = relationship("Booking", back_populates="user")

class FitnessClass(Base):
    """Fitness class model"""
    __tablename__ = "fitness_classes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dateTime = Column(DateTime, nullable=False)
    instructor = Column(String, nullable=False)
    availableSlots = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    bookings = relationship("Booking", back_populates="fitness_class")

class Booking(Base):
    """Booking model"""
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("fitness_classes.id"), nullable=False)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    booked_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    fitness_class = relationship("FitnessClass", back_populates="bookings")

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./fitness_studio.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
