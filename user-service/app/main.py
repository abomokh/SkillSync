from fastapi import FastAPI
from app.routes import auth, profile

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(profile.router, tags=["Profile"])
