from pwdlib import PasswordHash
import jwt
from datetime import datetime , timedelta , timezone
from jwt.exceptions import InvalidTokenError
from fastapi import Depends , HTTPException
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from database import get_db   
from sqlalchemy.orm import Session
from models import UserModel

# OAuth2_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/login")
security_scheme = HTTPBearer()

pwd_hash = PasswordHash.recommended()

password = "something123"

def hash_password_(password:str):
    return pwd_hash.hash(password)

def password_verification(password:str,hashed_pass : str):
    return pwd_hash.verify(password,hashed_pass)

SECRET_KEY = "SOMETHING_234@FHKRSKRH"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 30

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme),db:Session=Depends(get_db)): #token:str = Depends(OAuth2_scheme),
    token = credentials.credentials
    exception_error = HTTPException(
                    status_code= 401,
                    detail="invalid input"
                )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id : str = payload.get("sub")
        if user_id is None:
            raise exception_error
            
                
    except InvalidTokenError :
        raise exception_error

    user = db.get(UserModel, int(user_id))
    if user is None:
        raise exception_error
    return user
    