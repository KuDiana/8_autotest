import uuid

def generate_user():

    uid = uuid.uuid4().hex[:8]

    return {
        "username": f"test_{uid}",
        "email": f"{uid}@test.com",
        "password": "Test123!"
    }


# несуществующий пользователь (401)
invalid_user = {
    "username": "wrong_user",
    "password": "wrong_pass"
}


# (422)
invalid_payload = {
    "wrong": "data"
}