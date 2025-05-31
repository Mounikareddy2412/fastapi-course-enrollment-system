from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.auth import get_current_user  # ✅ Import the token-based user checker
from app.models import User

router = APIRouter()

@router.post("/enrollments/", response_model=schemas.EnrollmentOut)
def enroll_user(
    enrollment: schemas.EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ✅ Protect this route
):
    # Optional: Ensure the user is only enrolling themselves (for stricter auth)
    if enrollment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only enroll yourself")

    # Check if user exists
    db_user = crud.get_user(db, enrollment.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if course exists
    db_course = crud.get_course(db, enrollment.course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if already enrolled
    existing_enrollment = crud.get_enrollment_by_user_and_course(
        db, enrollment.user_id, enrollment.course_id
    )
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="User already enrolled in this course")

    return crud.create_enrollment(db, enrollment)

@router.get("/enrollments/", response_model=list[schemas.EnrollmentOut])
def read_enrollments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ✅ Protected GET route
):
    return crud.get_enrollments(db, skip=skip, limit=limit)
