import shopify
from database import get_token
from dotenv import load_dotenv
from fastapi import APIRouter #, Header #This is to look for JWT in the future
from routers.get_products import get_products
from helper.fetch_locations import get_shopify_locations
load_dotenv()

router = APIRouter()

@router.get("/get-all-inventory")
def get_inventory(shop: str):
    access_token = get_token(shop)
    if access_token == None:
        raise Exception("Store not found")
    api_version = "2024-01"
    full_product_list = get_products(shop) # Formatted as {Item Id: { id, title, variants: {variant1: {variant_id, sku, inventory_item_id}}}}
    all_locations = get_shopify_locations(shop) #Formatted as {Shop Name: Shop Id}
    #return all_locations
    with shopify.Session.temp(shop, api_version, access_token):
        levels = shopify.InventoryLevel.find(
            location_ids="110368522515, 110429110547",
            inventory_item_ids="54781037674771, 54781037707539, 54781037379859"
        )
        return [{"location_id": level.location_id, "available": level.available} for level in levels]
        #Create a loop to go through all locations, then find all product variant inventory_item_ids