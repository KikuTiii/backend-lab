from itertools import count

from schemas import OrderInput, OrderOutput


class OrderRepository:
    def __init__(self) -> None:
        self._orders: dict[int, OrderOutput] = {}
        self._order_ids = count(1)

    def save(self, order: OrderInput) -> OrderOutput:
        created = OrderOutput(
            id=next(self._order_ids),
            status="created",
            **order.model_dump(),
        )
        self._orders[created.id] = created

        return created

    def get_by_id(self, order_id: int) -> OrderOutput | None:
        return self._orders.get(order_id)
