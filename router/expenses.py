from fastapi import APIRouter
from schemas import AddRequest , ResponseModel , AddResponse
from database import db , cursor
from fastapi import HTTPException

router = APIRouter()


@router.get("/")
def home_page():
    return "WELCOME TO HOME PAGE"


@router.post("/expenses", response_model = AddResponse ) #output tuple ke form me hoga , we want in form of JSON , isliye we use , response_model = AddResponse 
def Add_Expense(userdata : AddRequest): 
    sql = """INSERT INTO Expenses
    (amount,category,description)
    VALUES (%s,%s,%s)
    """
    values = (userdata.amount,userdata.category,userdata.description)

    cursor.execute(sql,values)
    db.commit()

    return {"message":"Expense added Successfully",
            "id": cursor.lastrowid,
            "amount" : userdata.amount,
            "category" : userdata.category,
            "description": userdata.description
               }

@router.get("/expenses", response_model = list[ResponseModel]) #yaha multiple rows ayyegi isliye list use krna
def get_expenses():
    cursor.execute("SELECT * FROM Expenses")
    result = cursor.fetchall()
    return result

@router.get("/expenses/{id}",response_model = ResponseModel) # ResponseModel = 1 expense , list[ResponseModel] = multiple exp
def get_expense(id : int):
    sql = """SELECT * FROM Expenses
    where id = %s """
    values = (id,)
    cursor.execute(sql,values)
    result = cursor.fetchone()

    if result == None:
        raise HTTPException(
            status_code=404,
            detail="expense id not exsist"
        )
    
    return result

@router.put("/expenses/{id}")
def update_expense(id : int , new_data : AddRequest):
    sql = """SELECT * FROM Expenses
    WHERE id = %s 
    """
    values = (id,)
    cursor.execute(sql,values)
    result = cursor.fetchone()

    if result == None:
        raise HTTPException(
            status_code=404,
            detail="id does not exist"
        )

    sql = """UPDATE Expenses
    SET amount = %s,
    category = %s,
    description = %s
    WHERE id = %s
    """
    values = (new_data.amount, new_data.category, new_data.description, id)
    cursor.execute(sql,values)
    db.commit()

    return {
    "message": "Successfully updated",
    "id": id,
    "amount": new_data.amount,
    "category": new_data.category,
    "description": new_data.description
    }


@router.delete("/expenses/{id}")
def delete_expense(id:int):
    sql = """SELECT * FROM Expenses
        WHERE id = %s 
        """
    values = (id,)
    cursor.execute(sql,values)
    result = cursor.fetchone()
    
    if result == None:
        raise HTTPException(
            status_code=404,
            detail="id does not exist"  
        )

    sql = """DELETE FROM Expenses 
    WHERE id = %s """
    values = (id,)

    cursor.execute(sql,values)
    db.commit()
    return {"message":"Successfully deleted that id"}


