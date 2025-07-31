from fastapi import FastAPI,HTTPException
from fastapi.responses import RedirectResponse
import httpx
import os
from db.mongo import users_collection
from models.user import UserLogin,UserRegister
from utils.hashing import verify_password,hash_password
from utils.jwt_handler import create_access_token
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
def login():
    fb_oauth_url = (
        "https://www.facebook.com/v19.0/dialog/oauth"
        f"?client_id={FB_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=whatsapp_business_management,pages_messaging,business_management"
        f"&response_type=code"
    )
    return RedirectResponse(fb_oauth_url)

@app.get("/oauth/callback")
async def fb_callback(code: str):
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
        access_token = token_data.get("access_token")

        me_res = await client.get(
            f"https://graph.facebook.com/me?access_token={access_token}"
        )
        me = me_res.json()
        fb_user_id = me["id"]

        # Optional: fetch WABA info
        # For now just store access token and ID
        existing = users_collection.find_one({"fb_user_id": fb_user_id})
        if not existing:
            users_collection.insert_one({
                "name": me.get("name", "FB User"),
                "fb_user_id": fb_user_id,
                "fb_access_token": access_token,
                "loginMethod": "facebook"
            })

        return {"message": "Login successful!", "fb_user_id": fb_user_id}
