BOOK = {
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "isbn": "9780132350884",
    "published_year": 2008,
}


def test_hello_world(client):
    assert client.get("/").json() == {"message": "Hello, World!"}


def test_create_and_get_book(client):
    created = client.post("/books", json=BOOK)
    assert created.status_code == 201
    body = created.json()
    assert body["id"] == 1 and body["title"] == BOOK["title"]

    fetched = client.get(f"/books/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["isbn"] == BOOK["isbn"]


def test_duplicate_isbn_returns_409(client):
    client.post("/books", json=BOOK)
    assert client.post("/books", json=BOOK).status_code == 409


def test_validation_error_returns_422(client):
    assert client.post("/books", json={**BOOK, "title": ""}).status_code == 422


def test_list_with_pagination(client):
    for i in range(3):
        client.post("/books", json={**BOOK, "isbn": f"97801323508{i:02d}"})
    assert len(client.get("/books").json()) == 3
    assert len(client.get("/books?skip=1&limit=1").json()) == 1


def test_put_replaces_book(client):
    book_id = client.post("/books", json=BOOK).json()["id"]
    new = {**BOOK, "title": "Clean Code, 2nd ed.", "published_year": None}
    res = client.put(f"/books/{book_id}", json=new)
    assert res.status_code == 200
    assert res.json()["title"] == "Clean Code, 2nd ed."
    assert res.json()["published_year"] is None


def test_patch_updates_only_sent_fields(client):
    book_id = client.post("/books", json=BOOK).json()["id"]
    res = client.patch(f"/books/{book_id}", json={"author": "Uncle Bob"})
    assert res.status_code == 200
    assert res.json()["author"] == "Uncle Bob"
    assert res.json()["title"] == BOOK["title"]


def test_delete_book(client):
    book_id = client.post("/books", json=BOOK).json()["id"]
    assert client.delete(f"/books/{book_id}").status_code == 204
    assert client.get(f"/books/{book_id}").status_code == 404


def test_missing_book_returns_404(client):
    assert client.get("/books/999").status_code == 404
    assert client.put("/books/999", json=BOOK).status_code == 404
