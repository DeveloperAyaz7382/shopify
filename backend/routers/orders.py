# # backend/routers/orders.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from models import Order as DBOrder
# from schemas import OrderCreate, Order
# from database import get_db  # Make sure to import the database session dependency
# from database import SessionLocal

# # Create an APIRouter instance
# router = APIRouter()

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @router.post("/", response_model=Order)
# def create_order(order: OrderCreate, db: Session = Depends(get_db)):
#     # Validate the status field before attempting to insert into the database
#     if order.status not in ['pending', 'shipped', 'delivered']:
#         raise HTTPException(status_code=400, detail="Invalid order status")

#     db_order = DBOrder(
#         user_id=order.user_id,
#         status=order.status,
#         total_amount=order.total_amount
#     )
#     db.add(db_order)
#     db.commit()
#     db.refresh(db_order)

#     return db_order

# # Add more routes as needed, for example:
# @router.get("/{order_id}", response_model=Order)
# def get_order(order_id: int, db: Session = Depends(get_db)):
#     db_order = db.query(DBOrder).filter(DBOrder.id == order_id).first()
#     if db_order is None:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return db_order
