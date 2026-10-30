from repositories.order_repository import OrderRepository
from schemas import OrderInput


def test_save_and_get_order():
    repository = OrderRepository()

    order = OrderInput(
        customer_id=42,
        product_id=10,
        quantity=2,
    )

    created = repository.save(order)

    assert created.id > 0
    assert created.customer_id == 42
    assert created.product_id == 10
    assert created.quantity == 2
    assert created.status == "created"
    assert repository.get_by_id(created.id) == created


def test_save_generates_unique_ids():
    repository = OrderRepository()

    order = OrderInput(
        customer_id=42,
        product_id=10,
        quantity=2,
    )

    first = repository.save(order)
    second = repository.save(order)

    assert first.id != second.id


def test_get_nonexistent_order():
    repository = OrderRepository()

    assert repository.get_by_id(999) is None
