from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import httpx
import os

load_dotenv()

app = FastAPI()

FB_CLIENT_ID = os.getenv("FB_CLIENT_ID")
FB_CLIENT_SECRET = os.getenv("FB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@app.get("/")
def home():
    return {"message": "Go to /login to start OAuth flow"}

@app.get("/login")
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
async def oauth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing 'code' parameter"}

    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            "https://graph.facebook.com/v19.0/oauth/access_token",
            params={
                "client_id": FB_CLIENT_ID,
                "client_secret": FB_CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code,
            },
        )
        token_data = token_res.json()

    return {"token_data": token_data}
