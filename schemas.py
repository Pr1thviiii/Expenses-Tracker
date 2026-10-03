from pydantic import BaseModel,ConfigDict

class AddRequest(BaseModel): 
    amount : float
    category : str 
    description : str

class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    amount : float
    category : str 
    description : str

class UserRegister(BaseModel):
    email : str
    password : str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    email : str

class Token(BaseModel):
    access_token : str
    token_type : str
