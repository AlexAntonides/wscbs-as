import json
import pytest 

from app import app as application, validate_token
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
def test_main_post(client):
    response = client.post("/users", data=json.dumps({ 'username': USERNAME, 'password': PASSWORD }), content_type='application/json')
    assert response.status_code == HTTPStatus.OK

# ----- Login -----
def test_login_post(client):
    response = client.post("/users/login", data=json.dumps({ 'username': USERNAME, 'password': PASSWORD }), content_type='application/json')
    
    sub = validate_token(response.data)

    assert response.status_code == HTTPStatus.OK
    assert sub == USERNAME

def test_login_faulty_password_post(client):
    response = client.post("/users/login", data=json.dumps({ 'username': USERNAME, 'password': 'wrong_password' }), content_type='application/json')

    assert response.status_code == HTTPStatus.FORBIDDEN

def test_login_faulty_username_post(client):
    response = client.post("/users/login", data=json.dumps({ 'username': 'wrong_username', 'password': PASSWORD }), content_type='application/json')

    assert response.status_code == HTTPStatus.FORBIDDEN