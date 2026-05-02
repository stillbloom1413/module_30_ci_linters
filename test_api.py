from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
created_recipe_id = None


def test_create_recipe():
    global created_recipe_id
    with TestClient(app) as client:
        response = client.post(
            "/recipes",
            json={
                "name": "Хлеб",
                "cooking_time": 1,
                "ingredients": "Хлеб",
                "description": "Балдеж",
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Хлеб"
    created_recipe_id = data["id"]


def test_get_recipe():
    with TestClient(app) as client:
        response = client.get(f"/recipes/{created_recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_recipe_id


def test_get_recipe_error():
    with TestClient(app) as client:
        response = client.get("/recipes/99999999")
    assert response.status_code == 404


def test_get_recipes_list():
    with TestClient(app) as client:
        response = client.get("/recipes")
    assert response.status_code == 200
