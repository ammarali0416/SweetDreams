from fastapi import FastAPI
from routers.openai import router as openai_router


app = FastAPI()

app.include_router(openai_router)