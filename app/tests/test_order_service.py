"""Testes unitários do OrderService, isolado do repositório real por um fake."""
import pytest
from pydantic import ValidationError

from schemas import OrderInput, OrderOutput
from services.order_service import (
    MAX_ORDER_QUANTITY,
    OrderService,
    QuantityLimitExceededError,
)


class FakeOrderRepository:
    def __init__(self) -> None:
        self.orders: dict[int, OrderOutput] = {}
        self.save_calls = 0

    def save(self, order: OrderOutput) -> None:
        self.orders[order.id] = order
        self.save_calls += 1

    def get_by_id(self, order_id: int) -> OrderOutput | None:
        return self.orders.get(order_id)


def test_create_order_saves_once():
    repository = FakeOrderRepository()
    service = OrderService(repository)

    order = OrderInput(
        customer_id=42,
        product_id=10,
        quantity=2,
    )

    created = service.create_order(order)

    assert created.status == "created"
    assert repository.save_calls == 1
    assert repository.get_by_id(created.id) == created


def test_invalid_order_does_not_save():
    repository = FakeOrderRepository()
    service = OrderService(repository)

    order = OrderInput(
        customer_id=42,
        product_id=10,
        quantity=101,
    )

    with pytest.raises(QuantityLimitExceededError):
        service.create_order(order)

    assert repository.save_calls == 0
    assert repository.orders == {}


def test_get_nonexistent_order_returns_none():
    repository = FakeOrderRepository()
    service = OrderService(repository)

    assert service.get_order(999999) is None


# Testes de limite (boundary testing) da quantidade

def test_quantity_zero_is_rejected_by_schema():
    with pytest.raises(ValidationError):
        OrderInput(customer_id=42, product_id=10, quantity=0)


@pytest.mark.parametrize("quantity", [1, MAX_ORDER_QUANTITY])
def test_quantity_within_limits_is_accepted(quantity):
    repository = FakeOrderRepository()
    service = OrderService(repository)

    order = OrderInput(customer_id=42, product_id=10, quantity=quantity)

    created = service.create_order(order)

    assert created.quantity == quantity
    assert repository.save_calls == 1


def test_quantity_above_limit_is_rejected_by_service():
    repository = FakeOrderRepository()
    service = OrderService(repository)

    order = OrderInput(customer_id=42, product_id=10, quantity=MAX_ORDER_QUANTITY + 1)

    with pytest.raises(QuantityLimitExceededError):
        service.create_order(order)
