import os
import shopify
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from database import save_token
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.get("/auth")
def auth(shop: str):
    API_KEY = os.getenv("SHOPIFY_API_KEY")
    API_SECRET = os.getenv("SHOPIFY_API_SECRET")

    if not API_KEY or not API_SECRET:
        raise HTTPException(status_code=500, detail="API Key or Secret missing in .env")

    shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)

    session = shopify.Session(shop, "2024-01")

    app_url = os.getenv("SHOPIFY_APP_URL")
    redirect_uri = f"{app_url}/auth/callback"
    scopes = ["read_products", "read_inventory"]
    permission_url = session.create_permission_url(scopes, redirect_uri)
    return RedirectResponse(permission_url)

@router.get("/auth/callback")
async def auth_callback(request: Request):
    params = dict(request.query_params)
    shop_url = params.get("shop")
    shopify.Session.setup(
        api_key=os.getenv("SHOPIFY_API_KEY"), 
        secret=os.getenv("SHOPIFY_API_SECRET")
    )
    session = shopify.Session(shop_url, "2024-01")
    
    try:
        access_token = session.request_token(params)
        save_token(shop_url, access_token)
        return {
            "status": "Success", 
        }
        
    except Exception as e:
        print(f"ERROR DURING TOKEN EXCHANGE: {e}")
        return {"error": str(e)}