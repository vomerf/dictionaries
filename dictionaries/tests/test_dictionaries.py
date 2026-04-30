import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_dictionaries_without_date(dictionary, versions):
    client = APIClient()

    response = client.get("/api/dictionaries/")

    assert response.status_code == 200
    data = response.data["dictionaries"]
    assert len(data) == 1
    assert data[0]["id"] == str(dictionary.id)


@pytest.mark.django_db
def test_dictionaries_with_valid_date(dictionary, versions):
    """Тест получения списка справочников с указанием будущей даты"""
    client = APIClient()

    response = client.get("/api/dictionaries/?date=2100-01-01")

    assert response.status_code == 200
    assert len(response.data["dictionaries"]) == 1


@pytest.mark.django_db
def test_dictionaries_with_past_date(dictionary, versions):
    """Тест получения списка справочников с указанием даты в прошлом"""
    client = APIClient()

    response = client.get("/api/dictionaries/?date=1900-01-01")

    assert response.status_code == 200
    assert response.data["dictionaries"] == []