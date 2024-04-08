from fastapi.testclient import TestClient
from pytest import fixture

from fastapi_do_zero.app import app


@fixture
def client():
    return TestClient(app)
