from fastapi import FastAPI,HTTPException,Depends
from fastapi.responses import RedirectResponse
import httpx
import os
from db.mongo import users_collection
from models.user import UserLogin,UserRegister
from utils.hashing import verify_password,hash_password
from utils.jwt_handler import create_access_token,verify_token
from pymongo.errors import DuplicateKeyError

app = FastAPI()

FB_CLIENT_ID = os.getenv("FB_CLIENT_ID")
FB_CLIENT_SECRET = os.getenv("FB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@app.get("/")
def home():
    return {"message": "Go to /login to start OAuth flow"}

@app.get("/login")
async def login(user : UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"user_id": str(db_user["_id"])})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/register")
async def register(user: UserRegister):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    new_user = {
        "email": user.email,
        "password": hashed_password,
    }

    try:
        users_collection.insert_one(new_user)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already registered")

    return {"message": "User registered successfully"}



@app.get("/connect/facebook")
def connect_to_fb(user_data=Depends(verify_token)):
    fb_oauth_url = (
        "https://www.facebook.com/v19.0/dialog/oauth"
        f"?client_id={FB_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=whatsapp_business_management,pages_messaging,business_management"
        f"&response_type=code"
    )
    return RedirectResponse(fb_oauth_url)

@app.get("/oauth/callback")
async def fb_callback(code: str ,user_data= Depends(verify_token)):
    # test_email = "john@example.com"  # Use this for testing

    token_url = (
        f"https://graph.facebook.com/v19.0/oauth/access_token"
        f"?client_id={FB_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&client_secret={FB_CLIENT_SECRET}"
        f"&code={code}"
    )

    async with httpx.AsyncClient() as client:
        token_res = await client.get(token_url)
        token_data = token_res.json()
        if token_res.status_code != 200 or "access_token" not in token_data:
            raise HTTPException(status_code=400, detail="Failed to get Facebook access token")

        access_token = token_data["access_token"]

        # Get Facebook user info
        me_res = await client.get(
            f"https://graph.facebook.com/me?access_token={access_token}"
        )
        me = me_res.json()
        if me_res.status_code != 200 or "id" not in me:
            raise HTTPException(status_code=400, detail="Failed to fetch Facebook profile")

        fb_user_id = me["id"]

        # Update the test user's record
        result = users_collection.update_one(
            {"email": user_data["email"]},  
            {
                "$set": {
                    "fb_user_id": fb_user_id,
                    "fb_access_token": access_token,
                    "name": me.get("name", "FB User"),
                }
            }
        )
        if result.modified_count:
            return {"message": "Facebook account linked successfully!"}
        else:
            raise HTTPException(status_code=500, detail="User update failed")
