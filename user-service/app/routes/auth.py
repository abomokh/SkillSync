from fastapi import APIRouter, HTTPException, status
from app.models.user import UserIn, UserOut, Token
from app.db.mongo import users_collection
from app.utils.auth import hash_password, verify_password, create_jwt

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserIn):
    # print("users_collection:",users_collection) # for debug
    # print("user.email:",user.email) # for debug
    existing = users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    user_doc = {"email": user.email, "password": hashed_pw}
    result = users_collection.insert_one(user_doc)
    return UserOut(id=str(result.inserted_id), email=user.email)


@router.post("/login", response_model=Token)
async def login(user: UserIn):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt(user.email)
    return Token(access_token=token)
