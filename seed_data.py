"""
Seed script to populate the database with sample data

Run this script to add sample users, classes, and bookings to your database.
This is helpful for testing and demonstration purposes.

Usage:
    python seed_data.py
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db, User, FitnessClass, Booking
from app.auth import get_password_hash
import pytz

IST = pytz.timezone('Asia/Kolkata')

def create_sample_users(db: Session):
    """Create sample users"""
    users = [
        {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "password": "password123"
        },
        {
            "name": "Bob Smith",
            "email": "bob@example.com",
            "password": "password123"
        },
        {
            "name": "Charlie Davis",
            "email": "charlie@example.com",
            "password": "password123"
        },
        {
            "name": "Diana Prince",
            "email": "diana@example.com",
            "password": "password123"
        }
    ]
    
    created_users = []
    for user_data in users:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if existing_user:
            print(f"⚠️  User {user_data['email']} already exists, skipping...")
            created_users.append(existing_user)
            continue
        
        user = User(
            name=user_data["name"],
            email=user_data["email"],
            hashed_password=get_password_hash(user_data["password"])
        )
        db.add(user)
        created_users.append(user)
        print(f"✅ Created user: {user_data['name']} ({user_data['email']})")
    
    db.commit()
    return created_users

def create_sample_classes(db: Session, users: list):
    """Create sample fitness classes"""
    base_time = datetime.now(IST)
    
    classes = [
        {
            "name": "Morning Yoga Flow",
            "dateTime": base_time + timedelta(days=1, hours=10),
            "instructor": "Sarah Williams",
            "availableSlots": 20
        },
        {
            "name": "HIIT Cardio Blast",
            "dateTime": base_time + timedelta(days=2, hours=18),
            "instructor": "Mike Johnson",
            "availableSlots": 15
        },
        {
            "name": "Zumba Dance Party",
            "dateTime": base_time + timedelta(days=3, hours=19),
            "instructor": "Maria Garcia",
            "availableSlots": 25
        },
        {
            "name": "Power Pilates",
            "dateTime": base_time + timedelta(days=4, hours=9),
            "instructor": "Emma Thompson",
            "availableSlots": 12
        },
        {
            "name": "Spin & Burn",
            "dateTime": base_time + timedelta(days=5, hours=17),
            "instructor": "David Lee",
            "availableSlots": 18
        },
        {
            "name": "Sunset Yoga",
            "dateTime": base_time + timedelta(days=6, hours=18, minutes=30),
            "instructor": "Sarah Williams",
            "availableSlots": 20
        },
        {
            "name": "CrossFit Fundamentals",
            "dateTime": base_time + timedelta(days=7, hours=6),
            "instructor": "Chris Martin",
            "availableSlots": 10
        },
        {
            "name": "Meditation & Mindfulness",
            "dateTime": base_time + timedelta(days=8, hours=8),
            "instructor": "Lisa Chen",
            "availableSlots": 30
        }
    ]
    
    created_classes = []
    for class_data in classes:
        # Create class with first user as creator
        fitness_class = FitnessClass(
            name=class_data["name"],
            dateTime=class_data["dateTime"].replace(tzinfo=None),  # Remove timezone for storage
            instructor=class_data["instructor"],
            availableSlots=class_data["availableSlots"],
            created_by=users[0].id
        )
        db.add(fitness_class)
        created_classes.append(fitness_class)
        print(f"✅ Created class: {class_data['name']} on {class_data['dateTime'].strftime('%Y-%m-%d %H:%M IST')}")
    
    db.commit()
    return created_classes

def create_sample_bookings(db: Session, users: list, classes: list):
    """Create sample bookings"""
    bookings = [
        # Alice books Yoga and HIIT
        {"user": users[0], "class": classes[0], "name": "Alice Johnson", "email": "alice@example.com"},
        {"user": users[0], "class": classes[1], "name": "Alice Johnson", "email": "alice@example.com"},
        
        # Bob books Zumba and Pilates
        {"user": users[1], "class": classes[2], "name": "Bob Smith", "email": "bob@example.com"},
        {"user": users[1], "class": classes[3], "name": "Bob Smith", "email": "bob@example.com"},
        
        # Charlie books Spin
        {"user": users[2], "class": classes[4], "name": "Charlie Davis", "email": "charlie@example.com"},
        
        # Diana books Yoga and Meditation
        {"user": users[3], "class": classes[0], "name": "Diana Prince", "email": "diana@example.com"},
        {"user": users[3], "class": classes[7], "name": "Diana Prince", "email": "diana@example.com"},
    ]
    
    for booking_data in bookings:
        # Check if booking already exists
        existing_booking = db.query(Booking).filter(
            Booking.user_id == booking_data["user"].id,
            Booking.class_id == booking_data["class"].id
        ).first()
        
        if existing_booking:
            print(f"⚠️  Booking already exists for {booking_data['name']} in {booking_data['class'].name}, skipping...")
            continue
        
        booking = Booking(
            user_id=booking_data["user"].id,
            class_id=booking_data["class"].id,
            client_name=booking_data["name"],
            client_email=booking_data["email"]
        )
        
        # Decrease available slots
        booking_data["class"].availableSlots -= 1
        
        db.add(booking)
        print(f"✅ Created booking: {booking_data['name']} → {booking_data['class'].name}")
    
    db.commit()

def seed_database():
    """Main function to seed the database"""
    print("\n🌱 Starting database seeding...\n")
    
    # Initialize database
    init_db()
    print("✅ Database initialized\n")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Create sample data
        print("👥 Creating sample users...")
        users = create_sample_users(db)
        print(f"\n✅ Created {len(users)} users\n")
        
        print("🏋️  Creating sample classes...")
        classes = create_sample_classes(db, users)
        print(f"\n✅ Created {len(classes)} fitness classes\n")
        
        print("📅 Creating sample bookings...")
        create_sample_bookings(db, users, classes)
        print("\n✅ Sample bookings created\n")
        
        print("=" * 60)
        print("🎉 Database seeding completed successfully!")
        print("=" * 60)
        print("\n📝 Sample Credentials:")
        print("-" * 60)
        print("Email: alice@example.com   | Password: password123")
        print("Email: bob@example.com     | Password: password123")
        print("Email: charlie@example.com | Password: password123")
        print("Email: diana@example.com   | Password: password123")
        print("-" * 60)
        print("\n💡 You can now login with any of these credentials!")
        print("🚀 Start the server: python run.py")
        print("📖 API Docs: http://localhost:8000/docs\n")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
