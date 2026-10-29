from typing import Protocol

from schemas import OrderOutput


class OrderRepositoryProtocol(Protocol):
    def save(self, order: OrderOutput) -> None:
        ...

    def get_by_id(self, order_id: int) -> OrderOutput | None:
        ...