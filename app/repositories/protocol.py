from typing import Protocol

from schemas import OrderOutput, OrderInput


class OrderRepositoryProtocol(Protocol):
    def save(self, order: OrderInput) -> OrderOutput:
        ...

    def get_by_id(self, order_id: int) -> OrderOutput | None:
        ...