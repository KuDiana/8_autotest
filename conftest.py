import pytest

from utils.api_client import register, login, get_profile, delete_user
from data.payload import generate_user
from config import ADMIN_USERNAME, ADMIN_PASSWORD


# Авторизация администратора
@pytest.fixture()
def admin_token():

    response = login({
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    })

    assert response.status_code == 200

    return response.json()["access_token"]


# ===== SETUP + TEARDOWN =====
@pytest.fixture()
def user_flow(admin_token):

    # 1. регистрация пользователя
    user = generate_user()

    reg = register(user)

    assert reg.status_code == 200

    # 2. login
    login_resp = login(user)

    assert login_resp.status_code == 200

    token = login_resp.json()["access_token"]

    # 3. получение profile id
    profile = get_profile(token)

    assert profile.status_code == 200

    user_id = profile.json()["profile"]["id"]

    yield {
        "user": user,
        "token": token,
        "id": user_id
    }

    delete_user(user_id, admin_token)