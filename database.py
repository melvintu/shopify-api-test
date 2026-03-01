from sqlalchemy import create_engine, Column, String, Boolean, DateTime, exc
from sqlalchemy.orm import declarative_base, sessionmaker, session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func

SQLALCHEMY_DATABASE_URL = "sqlite:///./shopify_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ShopifyShop(Base):
    __tablename__ = "shopify_shops"
    shop_url = Column(String, primary_key=True, index=True)
    access_token = Column(String, nullable=False)
    is_installed = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

def save_token(shop_url: str, access_token: str):
    if shop_url == None or access_token == None:
        raise ValueError("Shop url or access token cannot be None")
    db = SessionLocal()
    try:
        existing_shop = db.query(ShopifyShop).filter(ShopifyShop.shop_url == shop_url).first()
        if existing_shop:
            existing_shop.access_token = access_token
            existing_shop.is_installed = True
        else:
            new_shop = ShopifyShop(
                shop_url = shop_url,
                access_token = access_token
            )
            db.add(new_shop)
        db.commit()
        print(f"Successfully saved token for {shop_url} into the database")
    except Exception as e:
        print(f"Database Error: {e}")
        return {"error": str(e)}
    finally:
        db.close()

def get_token(shop_url: str):
    if shop_url == None:
        raise ValueError("Shop url cannot be None")
    db = SessionLocal()
    try:
        shop = db.query(ShopifyShop).filter(ShopifyShop.shop_url == shop_url).first()
        if shop:
            return shop.access_token
    except NoResultFound:
        print("No user found with that username")
    finally:
        db.close()  

Base.metadata.create_all(bind=engine)