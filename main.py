from fastapi import FastAPI
from router.exp_with_ORM import router as expense_router
from router.auth import router as auth_router
 
app = FastAPI()

app.include_router(expense_router)
app.include_router(auth_router)

