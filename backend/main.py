from fastapi import FastAPI
from routers import products
from routers import users
from routers.product_variants import router as product_variants_router
from routers.media_routes import router as media_router
from database import engine
import models

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the routers for products, orders, and users


app.include_router(users.router)
app.include_router(products.router)
app.include_router(media_router)
app.include_router(product_variants_router)
# app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shopify Admin Backend!"}

