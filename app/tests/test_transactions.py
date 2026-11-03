import os

import psycopg
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.integration
def test_transaction_rollback(clean_test_database):
    database_url = os.environ["TEST_DATABASE_URL"]

    with pytest.raises(psycopg.errors.CheckViolation):
        with psycopg.connect(database_url) as connection:
            connection.execute(
                """
                INSERT INTO orders (
                    customer_id, product_id, quantity, status
                )
                VALUES (%s, %s, %s, %s)
                """,
                (42, 10, 2, "created"),
            )

            connection.execute(
                """
                INSERT INTO orders (
                    customer_id, product_id, quantity, status
                )
                VALUES (%s, %s, %s, %s)
                """,
                (42, 10, -5, "created"),
            )

    with psycopg.connect(database_url) as connection:
        row = connection.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()

    assert row is not None
    assert row[0] == 0