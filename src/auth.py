from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET = "secret"
ALGO = "HS256"

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p):
    return pwd.hash(p)

def verify_password(p, h):
    return pwd.verify(p, h)

def create_token(user):
    return jwt.encode({
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }, SECRET, algorithm=ALGO)