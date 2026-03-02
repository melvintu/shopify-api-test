import shopify
from database import get_token
from dotenv import load_dotenv
load_dotenv()

def get_shopify_locations(shop: str):
    access_token = get_token(shop)
    if access_token == None:
        raise Exception("Store not found")
    api_version = "2024-01"
    with shopify.Session.temp(shop, api_version, access_token):    
        try:
            locations = shopify.Location.find()
            formatted_locations = {}
            for location in locations:
                formatted_locations[location.name] = location.id
            return formatted_locations
        except Exception as e:
            return {"error": str(e)}