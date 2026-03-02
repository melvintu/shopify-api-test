import shopify
from database import get_token
from dotenv import load_dotenv
from fastapi import APIRouter #, Header #This is to look for JWT in the future
from helper.fetch_products import fetch_products_from_shopify
load_dotenv()

router = APIRouter()

@router.get("/get-products")
def get_products(shop: str):
    products = fetch_products_from_shopify(shop)
    if isinstance(products, dict) and "error" in products:
        return products
    full_product_list = {}
    for p in products:
        variant_list = []
        for variant in p.variants:
            safe_variant_data = {
                "variant_id": variant.id,
                "sku": variant.sku,
                "inventory_item_id": variant.inventory_item_id,
            }
            variant_list.append(safe_variant_data)
        new_items = {"id" : p.id, "title" : p.title, "variants" : variant_list}
        full_product_list[p.id] = new_items
    return full_product_list