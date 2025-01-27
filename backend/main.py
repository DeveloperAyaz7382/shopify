from fastapi import FastAPI
from routers import products
from routers import users
# from routers.product_variants import router as product_variants_router
from database import engine
import models
from fastapi.middleware.cors import CORSMiddleware
from routers import media


# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Replace with your Vite frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the routers for products, orders, and users
app.include_router(users.router)
# app.include_router(products.router)
app.include_router(media.router, prefix="/media", tags=["media"])
# app.include_router(product_variants_router)
# app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shopify Admin Backend!"}


