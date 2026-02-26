import os
import uvicorn
from fastapi import FastAPI
import shopify
from routers.list_products import router as product_router

app = FastAPI()
app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "Main App is Running"}

if __name__ == "__main__":
    # Get the port from environment
    # or default to 8000
    current_port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=current_port)