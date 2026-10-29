from fastapi.testclient import TestClient
from main import app, order_repository


client = TestClient(app)


def test_create_order_success():
    payload = {
        "customer_id": 42,
        "product_id": 10,
        "quantity": 2,
    }

    response = client.post("/orders", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert isinstance(data["id"], int)
    assert data["customer_id"] == 42
    assert data["product_id"] == 10
    assert data["quantity"] == 2
    assert data["status"] == "created"


def test_invalid_quantity():
    payload = {
        "customer_id": 42,
        "product_id": 10,
        "quantity": -1,
    }

    response = client.post("/orders", json=payload)

    assert response.status_code == 422


def test_missing_customer_id():
    payload = {
        "product_id": 10,
        "quantity": 2,
    }

    response = client.post("/orders", json=payload)

    assert response.status_code == 422


def test_unique_order_ids():
    payload = {
        "customer_id": 42,
        "product_id": 10,
        "quantity": 2,
    }

    first = client.post("/orders", json=payload)
    second = client.post("/orders", json=payload)

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] != second.json()["id"]


def test_invalid_customer_id():
    response = client.post("/orders", json={
        "customer_id": -1,
        "product_id": 10,
        "quantity": 2
    })

    assert response.status_code == 422


def test_invalid_product_id():
    response = client.post("/orders", json={
        "customer_id": 42,
        "product_id": 0,
        "quantity": 2
    })

    assert response.status_code == 422



def test_order_is_stored():
    response = client.post("/orders", json={
        "customer_id": 42,
        "product_id": 10,
        "quantity": 2
    })

    assert response.status_code == 201

    created_order = response.json()
    order_id = created_order["id"]

    stored = order_repository.get_by_id(order_id)
    assert stored is not None
    assert stored.customer_id == 42
    assert stored.quantity == 2


def test_get_existing_order():
    payload = {
        "customer_id": 42,
        "product_id": 10,
        "quantity": 2,
    }

    created = client.post("/orders", json=payload)
    order_id = created.json()["id"]

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    assert response.json() == created.json()


def test_get_nonexistent_order():
    response = client.get("/orders/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_get_invalid_order_id():
    response = client.get("/orders/abc")

    assert response.status_code == 422


def test_order_quantity_exceeds_limit():
    payload = {
        "customer_id": 42,
        "product_id": 10,
        "quantity": 101,
    }

    response = client.post("/orders", json=payload)

    assert response.status_code in (400, 422)

def test_order_quantity_exceeds_limit():
    response = client.post("/orders", json={
        "customer_id": 42,
        "product_id": 10,
        "quantity": 101,
    })

    assert response.status_code == 422