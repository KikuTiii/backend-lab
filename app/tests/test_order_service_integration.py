"""Service + OrderRepository real (em memória): verifica a integração entre as camadas."""
import pytest

from repositories.order_repository import OrderRepository
from schemas import OrderInput
from services.order_service import (
    OrderService,
    QuantityLimitExceededError,
)


def test_service_creates_order():
    repository = OrderRepository()
    service = OrderService(repository)

    order = OrderInput(
        customer_id=42,
        product_id=10,
        quantity=2,
    )

    result = service.create_order(order)

    assert result.status == "created"
    assert repository.get_by_id(result.id) == result


def test_service_rejects_quantity_above_limit():
    repository = OrderRepository()
    service = OrderService(repository)

    order = OrderInput(
        customer_id=42,
        product_id=10,
        quantity=101,
    )

    with pytest.raises(QuantityLimitExceededError):
        service.create_order(order)
