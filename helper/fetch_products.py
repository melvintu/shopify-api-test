import shopify
from database import get_token
from dotenv import load_dotenv
load_dotenv()

def fetch_products_from_shopify(shop: str):
    access_token = get_token(shop)
    if access_token == None:
        raise Exception("Store not found")
    api_version = "2024-01"
    with shopify.Session.temp(shop, api_version, access_token):    
        try:
            products = shopify.Product.find()
            return products
        except Exception as e:
            return {"error": str(e)}