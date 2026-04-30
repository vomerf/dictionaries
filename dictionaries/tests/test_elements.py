import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_get_elements_version_2(dictionary, versions, items):
    client = APIClient()

    response = client.get(f"/api/dictionaries/{dictionary.id}/elements?version=2.0")

    assert response.status_code == 200
    assert len(response.data["elements"]) == 2

@pytest.mark.django_db
def test_get_elements_version_1(dictionary, versions):
    client = APIClient()

    response = client.get(f"/api/dictionaries/{dictionary.id}/elements?version=1.0")

    assert response.status_code == 200
    assert response.data["elements"] == []


@pytest.mark.django_db
def test_get_elements_future_version_not_used(dictionary, versions, items):
    """Тест получения элементов без указания версии, когда есть будущая версия"""
    client = APIClient()

    response = client.get(
        f"/api/dictionaries/{dictionary.id}/elements"
    )

    assert response.status_code == 200
    assert response.data["elements"] == [
        {"code": "A01", "value": "Item A"},
        {"code": "B01", "value": "Item B"},
    ]