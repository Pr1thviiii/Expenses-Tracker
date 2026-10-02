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



 