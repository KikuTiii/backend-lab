from itertools import count

from repositories.order_repository import OrderRepository
from schemas import OrderInput, OrderOutput

MAX_ORDER_QUANTITY = 100

order_ids = count(1)


class QuantityLimitExceededError(ValueError):
    def __init__(self, quantity: int, limit: int = MAX_ORDER_QUANTITY):
        self.quantity = quantity
        self.limit = limit
        super().__init__(f"Quantity {quantity} exceeds the limit of {limit}")

class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, order: OrderInput) -> OrderOutput:
        if order.quantity > MAX_ORDER_QUANTITY:
            raise QuantityLimitExceededError(order.quantity)

        new_order = OrderOutput(
            id=next(order_ids),
            status="created",
            **order.model_dump(),
        )
        self.repository.save(new_order)

        return new_order


    def get_order(self, order_id: int) -> OrderOutput | None:
        return self.repository.get_by_id(order_id)
