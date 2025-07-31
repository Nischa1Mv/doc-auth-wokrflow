from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import httpx
import os
from db.mongo import users_collection

app = FastAPI()

FB_CLIENT_ID = os.getenv("FB_CLIENT_ID")
FB_CLIENT_SECRET = os.getenv("FB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@app.get("/")
def home():
    return {"message": "Go to /login to start OAuth flow"}

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
