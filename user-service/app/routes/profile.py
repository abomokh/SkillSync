from fastapi import APIRouter, Depends, HTTPException, Header
from app.utils.auth import decode_jwt
from app.models.user import UserOut
from app.db.mongo import users_collection

router = APIRouter()

async def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise Exception("Invalid scheme")
        payload = decode_jwt(token)
        user = users_collection.find_one({"email": payload["sub"]})
        if not user:
            raise Exception("User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.get("/profile", response_model=UserOut)
async def profile(user=Depends(get_current_user)):
    print("DEBUG > hello from get(/profile)")   # DEBUG
    return UserOut(id=str(user["_id"]), email=user["email"])