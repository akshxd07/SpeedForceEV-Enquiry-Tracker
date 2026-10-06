import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_valid_enquiry():
    payload = {
        "customer_name": "Rohan Sharma",
        "phone": "9876543210",
        "city": "Vadodara",
        "vehicle_model": "Joy e-bike Monster",
        "notes": "Interested in test ride"
    }
    response = client.post("/enquiries", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Rohan Sharma"
    assert data["status"] == "New"

def test_create_invalid_phone():
    payload = {
        "customer_name": "Rahul Verma",
        "phone": "12345",
        "city": "Ahmedabad",
        "vehicle_model": "Joy e-bike Wolf"
    }
    response = client.post("/enquiries", json=payload)
    assert response.status_code == 422

def test_get_summary():
    response = client.get("/summary")
    assert response.status_code == 200
    data = response.json()
    assert "New" in data
    assert "Purchased" in data