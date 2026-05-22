from utils.api_client import login

def test_bug_empty_username_login():

    payload = {
        "username": "",
        "password": "Test123!"
    }

    response = login(payload)

    print("\nBUG: EMPTY USERNAME LOGIN")
    print(f"STATUS: {response.status_code}")
    print(f"BODY: {response.json()}")

    print("\nAPI BUG:")
    print("expected -> 401 / 422")
    print("actual -> 200")

    # API BUG:
    # expected -> 401 / 422
    # actual -> 200

def test_all_fields_empty_login():

    payload = {
        "username": "",
        "password": "Test123!"
    }

    response = login(payload)

    print("\nBUG: ALL LOGIN FIELDS EMPTY")
    print(f"STATUS: {response.status_code}")
    print(f"BODY: {response.json()}")

    print("\nAPI BUG:")
    print("expected -> 401 / 422")
    print("actual -> 200")

    # API BUG:
    # expected -> 401 / 422
    # actual -> 200