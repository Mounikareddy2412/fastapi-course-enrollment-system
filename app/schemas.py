from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# --- User Schemas ---
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# --- User Schemas ---

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "student"  # Allow role input; default is "student"

class UserOut(UserBase):
    id: int
    is_active: bool  # Ensure your model supports this field
    role: str        # Include role in API responses

    class Config:
        orm_mode = True

# --- Course Schemas ---

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[date] = None

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True


# --- Enrollment Schemas ---
class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentOut(EnrollmentBase):
    id: int

    class Config:
        orm_mode = True

# --- Token Schema for Authentication ---
class Token(BaseModel):
    access_token: str
    token_type: str



