from sqlalchemy import Column, Integer, String
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

# =====================
# BATCH MODEL
# =====================
class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    institution_id = Column(Integer)


# =====================
# SESSION MODEL
# =====================
class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    batch_id = Column(Integer)
    trainer_id = Column(Integer)