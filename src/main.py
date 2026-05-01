from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

# =====================
# DATABASE SETUP
# =====================
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# =====================
# MODELS
# =====================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    institution_id = Column(Integer)


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    batch_id = Column(Integer)
    trainer_id = Column(Integer)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    student_id = Column(Integer)
    status = Column(String)


Base.metadata.create_all(bind=engine)

# =====================
# APP
# =====================
app = FastAPI()

# =====================
# DB DEPENDENCY
# =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================
# JWT
# =====================
SECRET_KEY = "secret"
ALGORITHM = "HS256"

def create_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# =====================
# REQUEST SCHEMAS
# =====================
class SignupSchema(BaseModel):
    name: str
    email: str
    password: str
    role: str


class LoginSchema(BaseModel):
    email: str
    password: str


class BatchSchema(BaseModel):
    name: str
    institution_id: int


class SessionSchema(BaseModel):
    title: str
    batch_id: int
    trainer_id: int


class AttendanceSchema(BaseModel):
    session_id: int
    student_id: int
    status: str

# =====================
# RESPONSE SCHEMAS
# =====================
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class BatchOut(BaseModel):
    id: int
    name: str
    institution_id: int

    class Config:
        from_attributes = True


class SessionOut(BaseModel):
    id: int
    title: str
    batch_id: int
    trainer_id: int

    class Config:
        from_attributes = True


class AttendanceOut(BaseModel):
    id: int
    session_id: int
    student_id: int
    status: str

    class Config:
        from_attributes = True

# =====================
# HOME
# =====================
@app.get("/")
def home():
    return {"message": "API running"}

# =====================
# AUTH
# =====================
@app.post("/auth/signup", response_model=dict)
def signup(data: SignupSchema, db: Session = Depends(get_db)):
    user = User(**data.dict())
    db.add(user)
    db.commit()
    return {"message": "User created"}


@app.post("/auth/login", response_model=dict)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or user.password != data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token(user.id, user.role)
    return {"token": token}

# =====================
# BATCH
# =====================
@app.post("/batches", response_model=dict)
def create_batch(data: BatchSchema, db: Session = Depends(get_db)):
    batch = Batch(**data.dict())
    db.add(batch)
    db.commit()
    return {"message": "Batch created"}


@app.get("/batches", response_model=list[BatchOut])
def get_batches(db: Session = Depends(get_db)):
    return db.query(Batch).all()

# =====================
# SESSION
# =====================
@app.post("/sessions", response_model=dict)
def create_session(data: SessionSchema, db: Session = Depends(get_db)):

    batch = db.query(Batch).filter(Batch.id == data.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    session = SessionModel(**data.dict())
    db.add(session)
    db.commit()
    return {"message": "Session created"}


@app.get("/sessions", response_model=list[SessionOut])
def get_sessions(db: Session = Depends(get_db)):
    return db.query(SessionModel).all()

# =====================
# ATTENDANCE
# =====================
@app.post("/attendance", response_model=dict)
def mark_attendance(data: AttendanceSchema, db: Session = Depends(get_db)):

    session = db.query(SessionModel).filter(SessionModel.id == data.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    attendance = Attendance(**data.dict())
    db.add(attendance)
    db.commit()
    return {"message": "Attendance marked"}


@app.get("/attendance", response_model=list[AttendanceOut])
def get_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).all()