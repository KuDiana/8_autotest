from utils.api_client import get_profile


def test_get_user_profile(user_flow):

    token = user_flow["token"]

    response = get_profile(token)

    assert response.status_code == 200

    data = response.json()

    assert "profile" in data

    profile = data["profile"]

    assert profile["username"] == user_flow["user"]["username"]
    assert profile["email"] == user_flow["user"]["email"]

    assert "id" in profile
    assert "username" in profile
    assert "email" in profile
    assert "role_id" in profile
    assert "profile_id" in profile
    assert "is_active" in profile
    assert "created_at" in profile
    assert "updated_at" in profile
    assert "role" in profile

    assert "id" in profile["role"]
    assert "name" in profile["role"]
    assert "description" in profile["role"]

    print("\nUSER PROFILE")
    print(f"ID: {profile['id']}")
    print(f"Username: {profile['username']}")
    print(f"Email: {profile['email']}")
    print(f"Role ID: {profile['role_id']}")
    print(f"Role: {profile['role']['name']}")
    print(f"Role Description: {profile['role']['description']}")
    print(f"Is Active: {profile['is_active']}")
    print(f"Created At: {profile['created_at']}")
    print(f"Updated At: {profile['updated_at']}")
