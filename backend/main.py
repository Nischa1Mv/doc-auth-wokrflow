from fastapi import FastAPI,HTTPException,Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import httpx
import os
from db.mongo import users_collection
from models.user import UserLogin,UserRegister
from utils.hashing import verify_password,hash_password
from utils.jwt_handler import create_access_token,verify_token
from pymongo.errors import DuplicateKeyError

app = FastAPI()

# Allowed origins
origins = [
    "http://localhost:8081",   # Metro bundler / Expo web
    "https://yourdomain.com",  # your frontend prod domain
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],            # ["GET", "POST"] if you want to restrict
    allow_headers=["*"],            # e.g. ["Authorization", "Content-Type"]
)

FB_CLIENT_ID = os.getenv("FB_CLIENT_ID")
FB_CLIENT_SECRET = os.getenv("FB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@app.get("/")
def home():
    return {"message": "Go to /login to start OAuth flow"}

@app.post("/login")
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
def connect_to_fb():
# def connect_to_fb(user_data=Depends(verify_token)):
    fb_oauth_url = (
        "https://www.facebook.com/v19.0/dialog/oauth"
        f"?client_id={FB_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=public_profile,pages_show_list,pages_manage_posts,business_management,whatsapp_business_management"
        f"&response_type=code"
    )
    return RedirectResponse(fb_oauth_url)

@app.get("/oauth/callback")
async def fb_callback(code: str):
# async def fb_callback(code: str ,user_data= Depends(verify_token)):
    # test_email = "john@example.com"  # Use this for testing
    test_email = "sainischalmv@gmail.com"

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
            # {"email": user_data["email"]},  
            {"email": test_email},  
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

@app.get("/get-businesses")
async def get_businesses(access_token: str = Query(..., description="Facebook User Access Token")):
    url = f"https://graph.facebook.com/v19.0/me/businesses?access_token={access_token}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=data.get("error", "Failed to fetch businesses"))

        return {"businesses": data.get("data", [])}
    
#     {
#     "businesses": [
#         {
#             "id": "770556238835682",
#             "name": "Nischal Mantri"
#         },
#         {
#             "id": "755449053761891",
#             "name": "Nischal wokrplace"
#         }
#     ]
# }


@app.get("/get-waba-accounts")
async def get_waba_accounts(
    business_id: str = Query(..., description="Facebook Business ID"),
    access_token: str = Query(..., description="Facebook User Access Token")
):
    url = f"https://graph.facebook.com/v19.0/{business_id}/owned_whatsapp_business_accounts?access_token={access_token}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    try:
        data = response.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid JSON response from Facebook")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=data.get("error", "Failed to fetch WABA accounts"))

    return {"waba_accounts": data.get("data", [])}


@app.post("/subscribe-wba")
async def subscribe_waba(
    wba_id: str = Query(..., description="WhatsApp Business Account ID"),
    access_token: str = Query(..., description="Facebook User Access Token")
):
    url = f"https://graph.facebook.com/v19.0/{wba_id}/subscribed_apps?access_token={access_token}"

    async with httpx.AsyncClient() as client:
        response = await client.post(url)  # POST request

    try:
        data = response.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid JSON response from Meta API")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=data)

    return data

# VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")

# @app.get("/webhook")
# async def verify_webhook(
#     hub_mode: str = None,
#     hub_challenge: str = None,
#     hub_verify_token: str = None
# ):
#     if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
#         return int(hub_challenge)
#     raise HTTPException(status_code=403, detail="Verification failed")

# # 📩 Handle incoming WhatsApp webhook events
# @app.post("/webhook")
# async def webhook_listener(request: Request):
#     data = await request.json()

#     print("\n===== 📩 Incoming Webhook =====")
#     print(f"⏰ Timestamp: {datetime.utcnow().isoformat()} UTC")
#     print(f"🔍 Raw Data: {data}")

#     try:
#         # WhatsApp messages are nested inside "entry"
#         for entry in data.get("entry", []):
#             for change in entry.get("changes", []):
#                 value = change.get("value", {})
#                 messages = value.get("messages", [])
                
#                 for msg in messages:
#                     from_number = msg.get("from")
#                     msg_body = msg.get("text", {}).get("body", "")
#                     print(f"📨 Message from {from_number}: {msg_body}")

#     except Exception as e:
#         print("⚠️ Error parsing webhook:", e)

#     return {"status": "received"}
