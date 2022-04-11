import json
import pytest 

from user_service import app as application, SECRET_KEY, ALGORITHM
from http import HTTPStatus
import jwt

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
    response = client.post("/users", data=json.dumps({ 'username': USERNAME, 'password': PASSWORD }), content_type='application/json')
    assert response.status_code == HTTPStatus.OK

# ----- Login -----
def test_login_get(client):
    response = client.post("/users/login", data=json.dumps({ 'username': USERNAME, 'password': PASSWORD }), content_type='application/json')
    
    encoded_jwt = response.json
    token = jwt.decode(encoded_jwt, SECRET_KEY, algorithm=ALGORITHM)

    assert response.status_code == HTTPStatus.OK
    assert token.public_id == USERNAME