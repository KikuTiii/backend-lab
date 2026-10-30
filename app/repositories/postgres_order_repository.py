import psycopg
from psycopg.rows import dict_row

from schemas import OrderInput, OrderOutput


class PostgresOrderRepository:
    def __init__(self, database_url: str):
        self.database_url = database_url

    def save(self, order: OrderInput) -> OrderOutput:
        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                """
                INSERT INTO orders (customer_id, product_id, quantity)
                VALUES (%s, %s, %s)
                RETURNING id, customer_id, product_id, quantity, status
                """,
                (order.customer_id, order.product_id, order.quantity),
            ).fetchone()

        assert row is not None
        return OrderOutput(**row)

    def get_by_id(self, order_id: int) -> OrderOutput | None:
        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            row = connection.execute(
                """
                SELECT id, customer_id, product_id, quantity, status
                FROM orders
                WHERE id = %s
                """,
                (order_id,),
            ).fetchone()

        return OrderOutput(**row) if row else None
