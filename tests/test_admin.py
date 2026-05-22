from utils.api_client import (
    get_profile,
    get_profiles,
    change_role,
    register,
    login,
    delete_user
)

from config import ADMIN_USERNAME
from data.payload import generate_user


# =========================================================
# 0. ADMIN PROFILE
# =========================================================
def test_get_admin_profile(admin_token):

    response = get_profile(admin_token)

    assert response.status_code == 200

    data = response.json()

    assert "profile" in data

    profile = data["profile"]

    # проверка роли
    assert profile["role"]["name"] == "admin"

    # обязательные поля
    assert "id" in profile
    assert "username" in profile
    assert "email" in profile
    assert "role_id" in profile
    assert "profile_id" in profile
    assert "is_active" in profile
    assert "created_at" in profile
    assert "updated_at" in profile
    assert "role" in profile

    # поля роли
    assert "id" in profile["role"]
    assert "name" in profile["role"]
    assert "description" in profile["role"]

    print("\nADMIN PROFILE")

    print(f"ID: {profile['id']}")
    print(f"Username: {profile['username']}")
    print(f"Email: {profile['email']}")
    print(f"Role ID: {profile['role_id']}")
    print(f"Role: {profile['role']['name']}")
    print(f"Role Description: {profile['role']['description']}")
    print(f"Is Active: {profile['is_active']}")
    print(f"Created At: {profile['created_at']}")
    print(f"Updated At: {profile['updated_at']}")


# =========================================================
# 1. LIST USERS (ADMIN)
# =========================================================
def test_admin_get_all_profiles(admin_token):

    response = get_profiles(admin_token)

    assert response.status_code == 200

    data = response.json()

    if isinstance(data, list):
        users = data

    elif "profiles" in data:
        users = data["profiles"]

    else:
        users = []

    assert isinstance(users, list)

    print("\nALL USERS SUMMARY")
    print(f"Total users: {len(users)}")

    for u in users[:5]:

        assert "id" in u
        assert "username" in u

        print(f"- ID: {u.get('id')} | Username: {u.get('username')}")


# =========================================================
# 2. CHANGE ROLE
# =========================================================
def test_admin_change_user_role(user_flow, admin_token):

    user_id = user_flow["id"]

    response = change_role(user_id, "admin", admin_token)

    assert response.status_code == 200

    body = response.json()

    # если API возвращает detail/message → проверяем
    if "detail" in body:
        assert body["detail"] != ""

    updated_profile = get_profile(
        user_flow["token"]
    ).json()["profile"]

    role = updated_profile["role"]["name"]

    assert role == "admin"

    print("\nROLE CHANGE RESULT")
    print(f"User: {user_flow['user']['username']}")
    print(f"New role: {role}")


# =========================================================
# 3. ROLE ACCESS CHECK
# =========================================================
def test_admin_role_access(user_flow, admin_token):

    user_id = user_flow["id"]

    role_response = change_role(
        user_id,
        "admin",
        admin_token
    )

    assert role_response.status_code == 200

    response = get_profiles(user_flow["token"])

    assert response.status_code == 200

    data = response.json()

    if isinstance(data, list):
        users_count = len(data)

    elif "profiles" in data:
        users_count = len(data["profiles"])

    else:
        users_count = 0

    assert users_count > 0

    print("\nROLE ACCESS CHECK")
    print(f"User: {user_flow['user']['username']}")
    print(f"Visible users count: {users_count}")


# =========================================================
# 4. DELETE USER
# =========================================================
def test_admin_delete_user(admin_token):

    user = generate_user()

    register_response = register(user)

    assert register_response.status_code == 200

    login_resp = login(user)

    assert login_resp.status_code == 200

    token = login_resp.json()["access_token"]

    profile_resp = get_profile(token)

    assert profile_resp.status_code == 200

    profile = profile_resp.json()["profile"]

    user_id = profile["id"]

    # защита от удаления администратора
    assert user["username"] != ADMIN_USERNAME

    response = delete_user(user_id, admin_token)

    assert response.status_code == 200

    body = response.json()

    # проверка текстовки если присутствует
    if "detail" in body:
        assert body["detail"] != ""

    if "message" in body:
        assert body["message"] != ""

    print("\nUSER DELETED")
    print(f"Username: {user['username']}")
    print(f"ID: {user_id}")