from pydantic import BaseModel

class AddRequest(BaseModel):
    amount : float
    category : str 
    description : str

class ResponseModel(BaseModel):
    id : int
    amount : float
    category : str 
    description : str

class AddResponse(BaseModel):
    message : str
    id : int
    amount : float
    category : str 
    description : str