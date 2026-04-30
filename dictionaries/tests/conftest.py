import pytest
from datetime import date, timedelta

from dictionaries.models import (
    Dictionary,
    DictionaryVersion,
    DictionaryItem,
)


@pytest.fixture
def dictionary():
    return Dictionary.objects.create(
        code="TEST",
        name="Тестовый справочник"
    )


@pytest.fixture
def versions(dictionary):
    today = date.today()

    v1 = DictionaryVersion.objects.create(
        dictionary=dictionary,
        version="1.0",
        start_date=today - timedelta(days=10)
    )

    v2 = DictionaryVersion.objects.create(
        dictionary=dictionary,
        version="2.0",
        start_date=today - timedelta(days=1)
    )

    # будущая версия
    v_future = DictionaryVersion.objects.create(
        dictionary=dictionary,
        version="3.0",
        start_date=today + timedelta(days=10)
    )

    return {
        "v1": v1,
        "v2": v2,
        "future": v_future,
    }


@pytest.fixture
def items(versions):
    v2 = versions["v2"]

    return [
        DictionaryItem.objects.create(
            dictionary_version=v2,
            code="A01",
            value="Item A"
        ),
        DictionaryItem.objects.create(
            dictionary_version=v2,
            code="B01",
            value="Item B"
        ),
    ]