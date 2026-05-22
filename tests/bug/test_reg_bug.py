from utils.api_client import register
from data.payload import generate_user

import random
import string

def test_register_password_confirmation_mismatch(admin_token):

    user = generate_user()

    payload = {
        "username": user["username"],
        "email": user["email"],
        "password": "Test123!",
        "confirm_password": "Wrong123!"
    }

    response = register(payload)

    print("\nPASSWORD CONFIRMATION MISMATCH")
    print(f"STATUS: {response.status_code}")
    print(f"BODY: {response.json()}")

    print("\nAPI BUG:")
    print("expected -> validation error")
    print(f"actual -> {response.status_code}")

    # API BUG:
    # backend ignores confirm_password field


def test_register_password_confirmation_empty(admin_token):

    user = generate_user()

    payload = {
        "username": user["username"],
        "email": user["email"],
        "password": "Test123!",
        "confirm_password": ""
    }

    response = register(payload)

    print("\nPASSWORD CONFIRMATION EMPTY")
    print(f"STATUS: {response.status_code}")
    print(f"BODY: {response.json()}")

    print("\nAPI BUG:")
    print("expected -> validation error")
    print(f"actual -> {response.status_code}")

    # API BUG:
    # backend ignores confirm_password field

def test_register_empty_username(admin_token):

    user = generate_user()

    payload = {
        "username": "",
        "email": user["email"],
        "password": "Test123!"
    }

    response = register(payload)

    print("\nEMPTY USERNAME")
    print(f"STATUS: {response.status_code}")
    print(f"BODY: {response.json()}")

    print("\nAPI BUG:")
    print("expected -> validation error")
    print(f"actual -> {response.status_code}")
    print("Before successfully registered")

    # API BUG:
    # backend ignores EMPTY username field

def test_register_empty_password(admin_token):

    user = generate_user()

    payload = {
        "username": user["username"],
        "email": user["email"],
        "password": ""
    }

    response = register(payload)

    print("\nEMPTY USERNAME")
    print(f"STATUS: {response.status_code}")
    print(f"BODY: {response.json()}")

    print("\nAPI BUG:")
    print("expected -> validation error")
    print(f"actual -> {response.status_code}")

    # API BUG:
    # backend ignores EMPTY password field

def test_register_short_password(admin_token):

    user = generate_user()

    payload = {
        "username": user["username"],
        "email": user["email"],
        "password": "12345"
    }

    response = register(payload)

    print("\nSHORT PASSWORD")
    print(f"STATUS: {response.status_code}")
    print(f"BODY: {response.json()}")

    print("\nAPI BUG:")
    print("expected -> validation error")
    print(f"actual -> {response.status_code}")

    # API BUG:
    # backend allows short password (less than 6 characters)


def test_register_short_username(admin_token):

    user = generate_user()

    short_username = "u_" + random.choice(string.ascii_lowercase)

    payload = {
        "username": short_username,
        "email": user["email"],
        "password": "Test123!"
    }

    response = register(payload)

    print("\nSHORT USERNAME")
    print(f"STATUS: {response.status_code}")
    print(f"BODY: {response.json()}")

    print("\nAPI BUG:")
    print("expected -> validation error")
    print(f"actual -> {response.status_code}")

    # API BUG:
    # backend allows short username (less than 3 characters)


