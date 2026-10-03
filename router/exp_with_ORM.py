from fastapi import APIRouter , Depends , HTTPException
from database import get_db   
from sqlalchemy.orm import Session
from models import Expenses , UserModel
from sqlalchemy import select
from schemas import AddRequest ,ResponseModel
from auth_utils import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/",response_model=ResponseModel)
def add_exp(user_data:AddRequest ,db : Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_exp = Expenses(
        amount = user_data.amount ,
        category = user_data.category,
        description = user_data.description,
        user_id = current_user.id
    )
    
    db.add(new_exp)
    db.commit()    
    db.refresh(new_exp)

    return new_exp

@router.get("/",response_model=list[ResponseModel])
def get_all_expenses(db : Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    query = select(Expenses).where(Expenses.user_id == current_user.id)
    all_exp = db.scalars(query).all()
    return all_exp

@router.get("/{id}", response_model = ResponseModel)
def get_expense(id:int , db : Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    query = select(Expenses).where(Expenses.id == id ,Expenses.user_id == current_user.id)
    exp = db.scalars(query).first()
    if exp is None:
        raise HTTPException(
            status_code=404,
            detail="expense not found"
        )
    
    return exp

@router.put("/{id}",response_model = ResponseModel)
def update_exp(id : int,user_data:AddRequest,db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    query = select(Expenses).where(Expenses.id == id ,Expenses.user_id == current_user.id)
    exp = db.scalars(query).first()
    if exp is None:
        raise HTTPException(
            status_code=404,
            detail="expense not found"
        )
    
    exp.amount = user_data.amount
    exp.category = user_data.category
    exp.description = user_data.description
    db.commit()
    db.refresh(exp)

    return exp


@router.delete("/{id}")
def delete_exp(id:int,db:Session=Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    query = select(Expenses).where(Expenses.id == id,Expenses.user_id == current_user.id)
    exp = db.scalars(query).first()
    if exp is None:
        raise HTTPException(
            status_code=404,
            detail="expense not found"
        )

    db.delete(exp)
    db.commit()

    return {"message":"Successfully deleted"}

