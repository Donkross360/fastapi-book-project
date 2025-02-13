from tests import client


def test_get_all_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert isinstance(response.json(), dict)
    assert all(isinstance(k, str) and isinstance(v, dict) for k, v in response.json().items())


def test_get_single_book():
    response = client.get("/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Hobbit"
    assert data["author"] == "J.R.R. Tolkien"


def test_create_book():
    new_book = {
        "id": 4,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "publication_year": 1997,
        "genre": "Fantasy",
    }
    response = client.post("/books/", json=new_book)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 4
    assert data["title"] == "Harry Potter and the Sorcerer's Stone"
    expected_keys = {"id", "title", "author", "publication_year", "genre"}
    assert set(data.keys()) == expected_keys, f"Unexpected fields: {set(data.keys()) - expected_keys}"


def test_update_book():
    updated_book = {
        "id": 1,
        "title": "The Hobbit: An Unexpected Journey",
        "author": "J.R.R. Tolkien",
        "publication_year": 1937,
        "genre": "Fantasy",
    }
    response = client.put("/books/1", json=updated_book)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Hobbit: An Unexpected Journey"


def test_delete_book():
    response = client.delete("/books/3")
    assert response.status_code == 204

    response = client.get("/books/3")
    assert response.status_code == 404



def test_get_non_existent_book():
    response = client.get("/books/9999") 
    assert response.status_code == 404



def test_get_book_invalid_id():
    response = client.get("/books/abc") 
    assert response.status_code == 422

    response = client.get("/books/-1")  
    assert response.status_code == 404


def test_create_book_invalid_genre():
    invalid_data = {"title": "Test Book", "author": "John Doe", "genre": "InvalidGenre"}
    response = client.post("/books", json=invalid_data)
    assert response.status_code == 422

def test_create_book_malformed_request():
    missing_field_data = {"title": "Missing Author"}  
    response = client.post("/books", json=missing_field_data)
    assert response.status_code == 422

    wrong_type_data = {"title": 123, "author": "John Doe"} 
    response = client.post("/books", json=wrong_type_data)
    assert response.status_code == 422
