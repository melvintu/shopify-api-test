import shopify
import time
from database import get_token
from dotenv import load_dotenv
from fastapi import APIRouter # Header # This is to look for JWT in the future instead of shop URL
from routers.get_products import get_products
from helper.fetch_products import variants_into_string, variants_only_from_products
from helper.fetch_locations import get_shopify_locations, locations_into_string
load_dotenv()

router = APIRouter()

@router.get("/get-all-inventory")
def get_inventory_shopify(shop: str):
    access_token = get_token(shop)
    if access_token == None:
        raise Exception("Store not found")
    api_version = "2024-01"

    ## Prepare the products
    # Product list as {Item Id: { id, title, variants: {0 (a count for each variant): [{variant_id:..., sku:..., inventory_item_id:...}]}}}
    full_product_list = get_products(shop) 
    # Prepare a variants only list from full_product_list
    variants_only_list = variants_only_from_products(full_product_list)
    # Turn the variants list into a string to prepare for API call
    variants_string = variants_into_string(variants_only_list)

    ## Prepare the locations
    # All locations as {Shop Id: Shop Name}
    all_locations = get_shopify_locations(shop) 
    # All locations the dict into string to prepare for API call
    locations_string = locations_into_string(all_locations)

    ## Do shopify API call with fallback
    for attempt in range(3):
        try:
            with shopify.Session.temp(shop, api_version, access_token):
                levels = shopify.InventoryLevel.find(
                    location_ids=locations_string,
                    inventory_item_ids=variants_string
                )
            break
        except Exception as e:
            if attempt == 2:
                return {"error": str(e)}
            time.sleep(3)
    try:
        extracted_levels = [{"location_id": level.location_id, "amount": level.available, "variant_item_id": level.inventory_item_id} for level in levels]
    except Exception as e:
        return {"error": str(e)}
    
    ## Organise the final output
    formatted_output = []
    for levels in extracted_levels:
        item_id = levels["variant_item_id"]
        location_id = levels["location_id"]
        tmp_dict = {}
        if item_id in variants_only_list:
            if location_id in all_locations:
                levels["location_id"] = all_locations[location_id] # Change ID to name
                variant_info = variants_only_list[item_id]
                sku = variant_info["sku"] # Grab SKU
                tmp_dict["sku"] = sku
                tmp_dict.update(levels)
            
        formatted_output.append(tmp_dict)
    return formatted_output