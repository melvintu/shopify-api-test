import shopify
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/test")
#def get_shopify_products():
#    products = shopify.Product.find()
#    return [p.title for p in products]
async def request_to_shopify_req(request: Request):
    body = await request.body()
    return {
        "method": request.method,
        "headers": dict(request.headers),
        "url": str(request.url),
        "body": body.decode("utf-8") if body else "",
    }