import json
import pytest 

from user_service import app as application

USERNAME = "admin"
PASSWORD = "admin"

# ----- Setup -----
@pytest.fixture
def app():
    yield application

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

# ----- Main -----
def test_main_get(client):
    response = client.post("/users", data={ 'username': USERNAME, 'password': PASSWORD })
    assert response.status_code == 200