from fastapi import FastAPI
from router.exp_with_ORM import router





app = FastAPI()


app.include_router(router)

