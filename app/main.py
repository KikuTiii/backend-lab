import os

from dotenv import load_dotenv
from fastapi import FastAPI, status, HTTPException

from repositories.postgres_order_repository import PostgresOrderRepository
from schemas import OrderInput, OrderOutput
from services.order_service import OrderService, QuantityLimitExceededError

load_dotenv()

app = FastAPI()

order_repository = PostgresOrderRepository(os.environ["DATABASE_URL"])
order_service = OrderService(order_repository)

@app.post("/orders", status_code=status.HTTP_201_CREATED, response_model=OrderOutput)
def create_order(order: OrderInput):
    try:
        return order_service.create_order(order)
    except QuantityLimitExceededError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(error))

@app.get("/orders/{order_id}", response_model=OrderOutput)
def get_order(order_id: int):
    order = order_service.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
