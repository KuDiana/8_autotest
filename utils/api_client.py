import requests
from config import BASE_URL

def register(payload):
    return requests.post(f"{BASE_URL}/api/auth/register", json=payload)

def login(payload):
    return requests.post(f"{BASE_URL}/api/auth/login", json=payload)

def get_profile(token):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE_URL}/api/profiles/me", headers=headers)

def delete_user(user_id, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    return requests.delete(
        f"{BASE_URL}/api/profiles/{user_id}",
        headers=headers
    )

def get_profiles(token):
    headers = {"Authorization": f"Bearer {token}"}

    return requests.get(
        f"{BASE_URL}/api/profiles/",
        headers=headers
    )

def change_role(account_id, role_name, token):
    headers = {"Authorization": f"Bearer {token}"}

    return requests.put(
        f"{BASE_URL}/api/profiles/{account_id}/role",
        headers=headers,
        params={"role_name": role_name}
    )
