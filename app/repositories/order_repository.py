from schemas import OrderOutput


class OrderRepository:
    def __init__(self) -> None:
        self._orders: dict[int, OrderOutput] = {}

    def save(self, order: OrderOutput) -> None:
        self._orders[order.id] = order

    def get_by_id(self, order_id: int) -> OrderOutput | None:
        return self._orders.get(order_id)
