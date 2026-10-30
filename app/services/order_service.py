from repositories.protocol import OrderRepositoryProtocol
from schemas import OrderInput, OrderOutput

MAX_ORDER_QUANTITY = 100

class QuantityLimitExceededError(ValueError):
    def __init__(self, quantity: int, limit: int = MAX_ORDER_QUANTITY):
        self.quantity = quantity
        self.limit = limit
        super().__init__(f"Quantity {quantity} exceeds the limit of {limit}")

class OrderService:
    def __init__(self, repository: OrderRepositoryProtocol):
        self.repository = repository

    def create_order(self, order: OrderInput) -> OrderOutput:
        if order.quantity > MAX_ORDER_QUANTITY:
            raise QuantityLimitExceededError(order.quantity)

        return self.repository.save(order)

    def get_order(self, order_id: int) -> OrderOutput | None:
        return self.repository.get_by_id(order_id)
