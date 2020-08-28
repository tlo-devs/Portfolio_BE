import pytest
from django.test import Client


@pytest.fixture(scope="session")
def get_testing_client():
    cl = Client()
    return cl


@pytest.fixture(scope="module")
def get_storage_client():
    pass
