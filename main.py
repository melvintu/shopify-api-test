import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from routers.test_requests import router as test_router
from routers.get_products import router as test_products
from routers.get_auth import router as auth_router

load_dotenv()

app = FastAPI()
app.include_router(test_router)
app.include_router(test_products)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Main App is Running"}


if __name__ == "__main__":
    # Get the port from environment
    # or default to 8000
    current_port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=current_port)