import jwt
from typing import Annotated
from datetime import datetime, timedelta
import secrets
from fastapi import HTTPException,Depends,Request
from sqlalchemy import select
from models.user import User
from routers.engine import engine
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    secret = secrets.token_urlsafe(32)
    encoded_jwt = jwt.encode(to_encode, secret, algorithm="HS256")
    return encoded_jwt, secret


def verify_delta(decoded_jwt, delta: timedelta = timedelta(minutes=60)):
    if datetime.utcnow() < datetime.fromtimestamp(decoded_jwt["exp"]):
        raise HTTPException(status_code=401, detail="Token has expired")
    else:
        return decoded_jwt
    
    




def decode_access_token(request: Request,token: Annotated[str, Depends(oauth2_scheme)]):
    username = request.headers["username"]
    with engine.begin() as conn:
        try:
            stm = select(User).where(User.username == username)
            result = conn.execute(stm).fetchone()
            secret = result.user_secret
        except Exception as e:
            return {"error": str(e),"message":"problem fetching user secret"}
    try:
        decoded_jwt = jwt.decode(
            token, secret, algorithms=["HS256"])


        verify_delta(decoded_jwt)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    return "valid token"
