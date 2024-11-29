"""Tests for the books module."""

from src import VERSION

books_prefix = f"/api/{VERSION}/books"


def test_get_all_books(fake_session, fake_book_service, test_client):
    """Tests getting all books."""

    response = test_client.get(url=f"{books_prefix}")
    print(response)

    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)
