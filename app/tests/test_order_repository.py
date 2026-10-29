from repositories.order_repository import OrderRepository
from schemas import OrderOutput


def test_save_and_get_order():
    repository = OrderRepository()

    order = OrderOutput(
        id=1,
        customer_id=42,
        product_id=10,
        quantity=2,
        status="created",
    )

    repository.save(order)

    assert repository.get_by_id(1) == order


def test_get_nonexistent_order():
    repository = OrderRepository()

    assert repository.get_by_id(999) is None