import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_check_element_exists(dictionary, versions, items):
    client = APIClient()

    response = client.get(
        f"/api/dictionaries/{dictionary.id}/check-element",
        {
            "code": "A01",
            "value": "Item A"
        }
    )

    assert response.status_code == 200
    assert response.data["exists"] is True


@pytest.mark.django_db
def test_check_element_not_exists(dictionary, versions, items):
    client = APIClient()

    response = client.get(
        f"/api/dictionaries/{dictionary.id}/check-element",
        {
            "code": "XXX",
            "value": "Nope"
        }
    )

    assert response.status_code == 200
    assert response.data["exists"] is False


@pytest.mark.django_db
def test_check_element_with_version(dictionary, versions, items):
    client = APIClient()

    response = client.get(
        f"/api/dictionaries/{dictionary.id}/check-element",
        {
            "code": "A01",
            "value": "Item A",
            "version": "2.0"
        }
    )
    print(response.data)
    assert response.status_code == 200
    assert response.data["exists"] is True