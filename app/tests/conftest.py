import os

import psycopg
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def clean_test_database():
    database_url = os.environ["TEST_DATABASE_URL"]

    def clean():
        with psycopg.connect(database_url) as conn:
            if conn.info.dbname != "orders_test_db":
                raise RuntimeError(
                    "Refusing to clean a non-test database"
                )
            conn.execute("DELETE FROM orders")

    clean()

    try:
        yield
    finally:
        clean()