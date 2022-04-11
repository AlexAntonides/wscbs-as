import json
import pytest 

from url_shorterner_service import app as application, SHORT_URL_LEN

URL = "https://www.uva.nl/"

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
    LEN = 5
    for i in range(LEN):
        client.post("/", data=URL)

    response = client.get("/")
    assert response.status_code == 200
    assert len(json.loads(response.get_data(as_text=True))) == LEN

def test_main_post(client):
    response = client.post("/", data=URL)
    assert response.status_code == 201
    assert len(response.data) == SHORT_URL_LEN

def test_main_faulty_post(client):
    response = client.post("/")
    assert response.status_code == 400

def test_main_malformed_url(client):
    response = client.post("/", data="http://google")
    assert response.status_code == 400

def test_main_delete(client):
    response = client.delete("/")
    assert response.status_code == 404

# ----- Handle ID -----
def test_handle_id_get(client):
    main_response = client.post("/", data=URL)
    id = main_response.data.decode("utf-8")

    response = client.get(f"/{id}")
    assert response.status_code == 301

def test_handle_id_missing_get(client):
    response = client.get(f"/non-existant-id")
    assert response.status_code == 404

def test_handle_id_put(client):
    main_response = client.post("/", data=URL)
    id = main_response.data.decode("utf-8")

    response = client.put(f"/{id}", data="https://www.google.com/")
    assert response.status_code == 200

def test_handle_id_faulty_put(client):
    main_response = client.post("/", data=URL)
    id = main_response.data.decode("utf-8")

    response = client.put(f"/{id}")
    assert response.status_code == 400

def test_handle_id_missing_put(client):
    response = client.put(f"/non-existant-id")
    assert response.status_code == 404

def test_handle_id_delete(client):
    main_response = client.post("/", data=URL)
    id = main_response.data.decode("utf-8")

    response = client.delete(f"/{id}")
    assert response.status_code == 204

def test_handle_id_missing_delete(client):
    response = client.delete(f"/non-existant-id")
    assert response.status_code == 404
