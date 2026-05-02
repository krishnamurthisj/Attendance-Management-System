from fastapi import Depends, HTTPException, Header
from jose import jwt

SECRET = "secret"
ALGO = "HS256"

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing token")

    token = authorization.split(" ")[1]

    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])
    except:
        raise HTTPException(401, "Invalid token")

def require_role(role):
    def checker(user=Depends(get_current_user)):
        if user["role"] != role:
            raise HTTPException(403, "Forbidden")
        return user
    return checker