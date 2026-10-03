from fastapi import APIRouter
from schemas import UserRegister,UserResponse
from fastapi import Depends , HTTPException
from database import get_db   
from sqlalchemy.orm import Session
from models import UserModel
from sqlalchemy import select
from auth_utils import create_token, hash_password_, password_verification


router = APIRouter(prefix="/auth",tags=["Auth"])


@router.post("/register",response_model = UserResponse)
def registration(userdata:UserRegister, db:Session = Depends(get_db)):
    query = select(UserModel).where(UserModel.email == userdata.email)
    existing_user = db.scalars(query).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail= "email already exist"
        )

    hashed_pass__ = hash_password_(userdata.password)
   
    new_user = UserModel(
        email = userdata.email,
        hashed_pass = hashed_pass__
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login_(userdata:UserRegister,db:Session = Depends(get_db)):
    
    query = select(UserModel).where(UserModel.email == userdata.email )
    db_user = db.scalars(query).first()
    if db_user is None or not password_verification(userdata.password,db_user.hashed_pass):
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    data_pack = {"sub":str(db_user.id)}
    token = create_token(data=data_pack)
    return {"access_token": token, "token_type": "bearer"}