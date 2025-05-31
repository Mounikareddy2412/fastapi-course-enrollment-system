from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Boolean,Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base  # assuming you have Base in your database.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student")  # roles: student, instructor, admin
    is_active = Column(Boolean, default=True)  # ← Add this

    enrollments = relationship("Enrollment", back_populates="user")





class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    instructor_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(Date)

    instructor = relationship("User")
    enrollments = relationship("Enrollment", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    enrolled_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

