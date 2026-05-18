from utils.api_client import login, get_profile
from data.payload import invalid_user, invalid_payload


# 1. LOGIN SUCCESS + TOKEN
def test_login_success(user_flow):

    user = user_flow["user"]

    response = login(user)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["access_token"] != ""

    print("\nУспешная авторизация")
    print(f"Username: {user['username']}")
    print(f"Token: {data['access_token'][:25]}...")


# 2. SEND TOKEN (PROFILE)
def test_send_token(user_flow):

    token = user_flow["token"]

    response = get_profile(token)

    assert response.status_code == 200

    data = response.json()

    assert data["profile"]["id"] == user_flow["id"]

    print("\nТокен успешно отправлен")
    print(f"Profile ID: {data['profile']['id']}")
    print(f"Username: {data['profile']['username']}")


# 3. INVALID USER → 401
def test_invalid_user_login():

    response = login(invalid_user)

    assert response.status_code == 401

    print("\nПроверка незарегистрированного пользователя")
    print(f"Status code: {response.status_code}")


# 4. INVALID PAYLOAD → 422
def test_validation_error():

    response = login(invalid_payload)

    assert response.status_code == 422

    print("\nПроверка ошибки валидации")
    print(f"Status code: {response.status_code}")