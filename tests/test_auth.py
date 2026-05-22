from utils.api_client import login, get_profile
from data.payload import invalid_user, invalid_payload

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


def test_send_token(user_flow):

    token = user_flow["token"]

    response = get_profile(token)

    assert response.status_code == 200

    print("\nTOKEN ACCEPTED")
    print(f"Status code: {response.status_code}")


def test_invalid_user_login():

    response = login(invalid_user)

    assert response.status_code == 401

    body = response.json()

    assert "detail" in body
    assert body["detail"] == "Incorrect username or password"

    print("\nINVALID USER LOGIN")
    print(f"Status code: {response.status_code}")
    print(f"Body: {body}")


def test_validation_error():

    response = login(invalid_payload)

    assert response.status_code == 422

    body = response.json()

    assert "detail" in body

    detail = body["detail"]

    assert detail[0]["loc"] == ["body", "username"]
    assert detail[0]["msg"] == "Field required"

    assert detail[1]["loc"] == ["body", "password"]
    assert detail[1]["msg"] == "Field required"

    print("\nVALIDATION ERROR")
    print(f"Status code: {response.status_code}")
    print(f"Body: {body}")

def test_wrong_password(user_flow):

    payload = {
        "username": user_flow["user"]["username"],
        "password": "WrongPassword123!"
    }

    response = login(payload)

    assert response.status_code == 401

    body = response.json()

    assert "detail" in body
    assert body["detail"] == "Incorrect username or password"

    print("\nWRONG PASSWORD")
    print(f"Status code: {response.status_code}")
    print(f"Body: {body}")

def test_empty_password_login():

    payload = {
        "username": "test_user",
        "password": ""
    }

    response = login(payload)

    assert response.status_code == 401

    body = response.json()

    assert "detail" in body
    assert body["detail"] == "Incorrect username or password"

    print("\nEMPTY PASSWORD LOGIN")
    print(f"Status code: {response.status_code}")
    print(f"Body: {body}")





