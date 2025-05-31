from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from app.routers import auth as auth_router
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import os

from app.database import engine, Base, get_db
from app import crud, models, schemas
from app.routers import users, courses, enrollments

# --- JWT Configuration ---
SECRET_KEY = "your_secret_key"  # 🔐 Use environment variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- ⚠️ Development Only: Recreate DB Tables on Startup ---
RECREATE_DB = os.getenv("RECREATE_DB", "false").lower() == "true"
if RECREATE_DB:
    print("⚠️ Dropping and recreating all tables (development mode)")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
else:
    Base.metadata.create_all(bind=engine)

# --- FastAPI app ---
app = FastAPI()

# --- Register routers ---
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(auth_router.router)

# --- Root endpoint ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Online Course Enrollment API"}

# --- Token Creation Helper ---
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- /token Login Endpoint ---
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Optional: Recreate DB from endpoint (ONLY for dev/testing) ---
@app.post("/recreate-db", tags=["dev"])
def recreate_db(db: Session = Depends(get_db)):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"message": "All tables dropped and recreated (development only)"}
