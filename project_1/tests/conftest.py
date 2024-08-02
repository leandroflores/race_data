import pytest

@pytest.fixture
def constructor_data() -> dict:
    return {
        "constructorId": "1",
        "name": "Ferrari",
        "nationality": "Italy",
        "url": "",
    }