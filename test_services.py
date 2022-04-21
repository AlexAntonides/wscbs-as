import json
import pytest 
import requests
import faker

from http import HTTPStatus

BASE_URL = "http://localhost"

from faker import Faker
fake = Faker()

# ----- Main -----
def test_a_long_function_because_i_am_lazy():
    admin_username = fake.user_name()
    admin_password = fake.password()
    admin_create_response = requests.post(f"{BASE_URL}/users", json={ 'username': admin_username, 'password': admin_password })
    
    user_username = fake.user_name()
    user_password = fake.password()
    user_create_response = requests.post(f"{BASE_URL}/users", json={ 'username': user_username, 'password': user_password })

    assert admin_create_response.status_code == HTTPStatus.OK
    assert user_create_response.status_code == HTTPStatus.OK

    admin_login_response = requests.post(f"{BASE_URL}/users/login", json={ 'username': admin_username, 'password': admin_password })
    user_login_response = requests.post(f"{BASE_URL}/users/login", json={ 'username': user_username, 'password': user_password })

    assert admin_login_response.status_code == HTTPStatus.OK
    assert user_login_response.status_code == HTTPStatus.OK

    admin_token = admin_login_response.text
    user_token = user_login_response.text

    admin_url = fake.url()
    user_url = fake.url()

    admin_created_url_response = requests.post(f"{BASE_URL}", data=admin_url, headers={"Authorization": f"Bearer {admin_token}"})
    assert admin_created_url_response.status_code == HTTPStatus.CREATED

    user_created_url_response = requests.post(f"{BASE_URL}", data=user_url, headers={"Authorization": f"Bearer {user_token}"})
    assert user_created_url_response.status_code == HTTPStatus.CREATED

    admin_short_code = admin_created_url_response.text
    user_short_code = user_created_url_response.text

    user_put_admin_url_response = requests.put(f"{BASE_URL}/{admin_short_code}", data=user_url, headers={"Authorization": f"Bearer {user_token}"})
    assert user_put_admin_url_response.status_code == HTTPStatus.FORBIDDEN

    admin_put_admin_url_response = requests.put(f"{BASE_URL}/{admin_short_code}", data=admin_url, headers={"Authorization": f"Bearer {admin_token}"})
    assert admin_put_admin_url_response.status_code == HTTPStatus.OK
    