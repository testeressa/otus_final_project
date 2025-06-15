import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# Тесты метода GET
@pytest.mark.parametrize("post_id, expected_status", [
    (1, 200),
    (100, 200),
    (0, 404),  # несуществующий ID
    (101, 404),  # несуществующий ID
    ("abc", 404)  # невалидный ID
])
def test_get_post_by_id(post_id, expected_status):
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert "id" in response.json()
        assert response.json()["id"] == post_id

@pytest.mark.parametrize("user_id, expected_count", [
    (1, 10),          # валидный user_id
    (11, 0),          # у пользователя 11 нет постов
    (999, 0),         # несуществующий пользователь
    (-1, 0),          # отрицательный user_id
    (0, 0),           # нулевой user_id
    ("abc", 0)        # нечисловой user_id
])
def test_get_posts_by_user(user_id, expected_count):
    response = requests.get(f"{BASE_URL}/posts", params={"userId": user_id})
    assert response.status_code == 200
    assert len(response.json()) == expected_count
    if expected_count > 0:
        for post in response.json():
            assert post["userId"] == user_id

# Тесты метода POST
@pytest.mark.parametrize("data, expected_status", [
    ({"title": "foo", "body": "bar", "userId": 1}, 201),
    ({"title": "", "body": "bar", "userId": 1}, 201),  # пустой title допустим
    ({"body": "bar", "userId": 1}, 201),  # отсутствует title
    ({"title": "foo", "body": "bar"}, 201),  # отсутствует userId
    ({}, 201)  # пустой объект
])
def test_create_post(data, expected_status):
    response = requests.post(f"{BASE_URL}/posts", json=data)
    assert response.status_code == expected_status
    if data:
        for key in data:
            assert key in response.json()


@pytest.mark.parametrize("post_id, data, expected_status, expected_fields", [
    # Валидные случаи
    (1, {"title": "updated title"}, 200, {"title": "updated title"}),
    (1, {"body": "updated body"}, 200, {"body": "updated body"}),
    (1, {"title": "new", "body": "new"}, 200, {"title": "new", "body": "new"}),

    # Несуществующие ID
    (999, {"title": "updated"}, 200, {}),  # jsonplaceholder всегда возвращает 200

    # Невалидные данные
    (1, {"invalid_field": "value"}, 200, {}),  # лишние поля игнорируются
    (1, {}, 200, {}),  # пустой запрос

    # Граничные случаи
    (0, {"title": "updated"}, 200, {}),  # нулевой ID
    ("abc", {"title": "updated"}, 200, {}),  # строковый ID
])
def test_update_post(post_id, data, expected_status, expected_fields):
    response = requests.patch(f"{BASE_URL}/posts/{post_id}", json=data)
    assert response.status_code == expected_status

    if expected_status == 200:
        response_data = response.json()
        for field, expected_value in expected_fields.items():
            assert field in response_data
            assert response_data[field] == expected_value

        if post_id and isinstance(post_id, int) and 1 <= post_id <= 100:
            assert response_data["id"] == post_id

# Тесты метода DELETE
@pytest.mark.parametrize("post_id, expected_status", [
    (1, 200),       # валидный ID → 200 OK
    (100, 200),     # валидный ID → 200 OK
    (0, 200),       # несуществующий ID, но API всё равно вернёт 200
    (101, 200),     # несуществующий ID, но API всё равно вернёт 200
    ("abc", 200),   # невалидный ID, но API всё равно вернёт 200
    (-1, 200)       # отрицательный ID, но API всё равно вернёт 200
])
def test_delete_post(post_id, expected_status):
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == {}

# Остальные тесты
def test_post_structure():
    response = requests.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200
    post = response.json()
    assert set(post.keys()) == {"userId", "id", "title", "body"}
    assert isinstance(post["userId"], int)
    assert isinstance(post["id"], int)
    assert isinstance(post["title"], str)
    assert isinstance(post["body"], str)