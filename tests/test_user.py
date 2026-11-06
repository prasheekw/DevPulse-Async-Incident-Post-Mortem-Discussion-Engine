def test_register_user(client):
    payload = {
        "username": "pytest_user",
        "email": "pytest_user@example.com",
        "password": "testpassword123"
    }

    response = client.post("/register", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_user(client):
    payload = {
        "username": "duplicate_user",
        "email": "duplicate@example.com",
        "password": "testpassword123"
    }

    client.post("/register", json=payload)

    response = client.post("/register", json=payload)

    assert response.status_code == 409

def test_login_success(client):
    payload = {
        "username": "login_user",
        "email": "login_user@example.com",
        "password": "testpassword123"
    }

    client.post("/register", json=payload)

    response = client.post("/login", json={
        "username": payload["username"],
        "password": payload["password"]
    })

    assert response.status_code == 200
    assert response.json() 


def test_login_wrong_password(client):
    payload = {
        "username": "wrong_password_user",
        "email": "wrong_password_user@example.com",
        "password": "testpassword123"
    }

    client.post("/register", json=payload)

    response = client.post("/login", json={
        "username": payload["username"],
        "password": "incorrectpassword"
    })

    assert response.status_code == 401

def test_auth_without_token(client):
    response = client.get("/is_auth")

    assert response.status_code == 401


def test_auth_with_valid_token(client):
    payload = {
        "username": "auth_user",
        "email": "auth_user@example.com",
        "password": "testpassword123"
    }

    client.post("/register", json=payload)

    login_response = client.post("/login", json={
        "username": payload["username"],
        "password": payload["password"]
    })

    token = login_response.json()

    response = client.get(
        "/is_auth",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["username"] == payload["username"]


def test_auth_with_invalid_token(client):
    response = client.get(
        "/is_auth",
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401