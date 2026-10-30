import os

import pytest
from dotenv import load_dotenv

from schemas import OrderInput
from repositories.postgres_order_repository import PostgresOrderRepository

load_dotenv()


@pytest.mark.integration
def test_save_order_postgres():
    repository = PostgresOrderRepository(
        os.environ["DATABASE_URL"]
    )

    order = OrderInput(
        customer_id=42,
        product_id=10,
        quantity=2,
    )

    created = repository.save(order)

    assert created.id > 0
    assert created.customer_id == 42
    assert created.quantity == 2
    assert created.status == "created"


@pytest.mark.integration
def test_get_order_postgres():
    repository = PostgresOrderRepository(
        os.environ["DATABASE_URL"]
    )

    order = OrderInput(
        customer_id=42,
        product_id=10,
        quantity=2,
    )

    created = repository.save(order)

    retrieved = repository.get_by_id(created.id)

    assert retrieved == created


@pytest.mark.integration
def test_get_nonexistent_order_postgres():
    repository = PostgresOrderRepository(
        os.environ["DATABASE_URL"]
    )

    result = repository.get_by_id(-999999)

    assert result is None