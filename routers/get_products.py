import shopify
import os
from dotenv import load_dotenv
from fastapi import APIRouter
load_dotenv()

router = APIRouter()

@router.get("/get-products")
def get_products():
    print("getting products")

    shop_url = os.getenv("SHOPIFY_SHOP_DOMAIN")
    access_token = os.getenv("SHOPIFY_TOKEN")
    api_version = "2024-01"
    with shopify.Session.temp(shop_url, api_version, access_token):    
        try:
            products = shopify.Product.find()
            return [{"id": p.id, "title": p.title} for p in products]
        except Exception as e:
            return {"error": str(e)}
        
