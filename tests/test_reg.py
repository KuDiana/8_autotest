from utils.api_client import (
    register,
    login,
    get_profile,
    delete_user
)

from data.payload import generate_user

def test_register_success(admin_token):

    user = generate_user()

    response = register(user)

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Account registered successfully"
    assert "account" in data

    assert data["account"]["username"] == user["username"]
    assert data["account"]["email"] == user["email"]

    print("\nSUCCESS REGISTER")
    print(f"Username: {user['username']}")
    print(f"Email: {user['email']}")

    # Проверка что пользователь реально может войти

    login_response = login({
        "username": user["username"],
        "password": user["password"]
    })

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    profile_response = get_profile(token)

    assert profile_response.status_code == 200

    profile = profile_response.json()["profile"]

    print(f"Profile ID: {profile['id']}")

    delete_user(profile["id"], admin_token)


def test_register_duplicate_username(admin_token):

    user = generate_user()

    register(user)

    payload = {
        "username": user["username"],
        "email": generate_user()["email"],
        "password": "Test123!"
    }

    response = register(payload)

    assert response.status_code == 400

    body = response.json()

    assert "detail" in body

    assert body["detail"] == (
        "Username or email already exists"
    )

    print("\nDUPLICATE USERNAME")
    print(f"Status: {response.status_code}")
    print(f"Message: {body['detail']}")

    login_response = login({
        "username": user["username"],
        "password": user["password"]
    })

    if login_response.status_code == 200:

        token = login_response.json()["access_token"]

        profile = get_profile(token).json()["profile"]

        delete_user(profile["id"], admin_token)


def test_register_duplicate_email(admin_token):

    user = generate_user()

    register(user)

    payload = {
        "username": generate_user()["username"],
        "email": user["email"],
        "password": "Test123!"
    }

    response = register(payload)

    assert response.status_code == 400

    body = response.json()

    assert "detail" in body

    assert body["detail"] == (
        "Username or email already exists"
    )

    print("\nDUPLICATE EMAIL")
    print(f"Status: {response.status_code}")
    print(f"Message: {body['detail']}")


    login_response = login({
        "username": user["username"],
        "password": user["password"]
    })

    if login_response.status_code == 200:

        token = login_response.json()["access_token"]

        profile = get_profile(token).json()["profile"]

        delete_user(profile["id"], admin_token)


def test_register_invalid_email():

    user = generate_user()

    payload = {
        "username": user["username"],
        "email": "wrong_email",
        "password": user["password"]
    }

    response = register(payload)

    assert response.status_code == 422

    body = response.json()

    assert "detail" in body

    error_text = body["detail"][0]["msg"]

    assert error_text == (
        "value is not a valid email address: "
        "An email address must have an @-sign."
    )

    print("\nINVALID EMAIL")
    print(f"Status: {response.status_code}")
    print(f"Message: {error_text}")


def test_register_empty_email():

    user = generate_user()

    payload = {
        "username": user["username"],
        "email": "",
        "password": user["password"]
    }

    response = register(payload)

    assert response.status_code == 422

    body = response.json()

    assert "detail" in body

    error_text = body["detail"][0]["msg"]

    assert error_text == (
        "value is not a valid email address: "
        "An email address must have an @-sign."
    )

    print("\nEMPTY EMAIL")
    print(f"Status: {response.status_code}")
    print(f"Message: {error_text}")


def test_register_email_without_domain_dot():

    user = generate_user()

    payload = {
        "username": user["username"],
        "email": "69be4c20@test",
        "password": user["password"]
    }

    response = register(payload)

    assert response.status_code == 422

    body = response.json()

    assert "detail" in body

    error_text = body["detail"][0]["msg"]

    assert error_text == (
        "value is not a valid email address: "
        "The part after the @-sign is not valid. "
        "It should have a period."
    )

    print("\nEMAIL WITHOUT DOMAIN DOT")
    print(f"Status: {response.status_code}")
    print(f"Message: {error_text}")


def test_register_email_ends_with_dot():

    user = generate_user()

    payload = {
        "username": user["username"],
        "email": "69be4c20@test.",
        "password": user["password"]
    }

    response = register(payload)

    assert response.status_code == 422

    body = response.json()

    assert "detail" in body

    error_text = body["detail"][0]["msg"]

    assert error_text == (
        "value is not a valid email address: "
        "An email address cannot end with a period."
    )

    print("\nEMAIL ENDS WITH DOT")
    print(f"Status: {response.status_code}")
    print(f"Message: {error_text}")

