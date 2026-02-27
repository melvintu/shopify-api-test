import shopify
from fastapi import APIRouter, Request, HTTPException
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

@router.get("/get-products")
def get_products():
    print("getting products")

    try:
        products = shopify.Product.find(limit=5)
        return [{"id": p.id, "title": p.title} for p in products]
    except Exception as e:
        return {"error": str(e)}
    
