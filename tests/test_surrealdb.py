"""Test the SurrealDB class."""
from __future__ import annotations
from unittest import mock

import pytest

from surrealdb import AuthenticationError, QueryError, SurrealDB


MOCK_200 = mock.Mock(
    status_code=200,
    json=mock.Mock(
        return_value=[
            {
                "status": "OK",
                "result": [
                    {
                        "id": "1",
                        "name": "test",
                    },
                ],
            }
        ],
    ),
)


def test_surrealdb_headers():
    """Test the headers of the SurrealDB class."""
    client = SurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    )
    assert client.headers == {
        "Content-Type": "application/json",
        "NS": "test",
        "DB": "test",
    }


def test_signin():
    """Test the signin method of the SurrealDB class."""
    with SurrealDB() as client:
        client.signin("admin", "admin")


def test_signup():
    """Test the signup method of the SurrealDB class."""
    with SurrealDB() as client:
        client.signup("admin", "admin")


def test_use():
    """Test the use method of the SurrealDB class."""
    with SurrealDB() as client:
        client.use("test", "test")

        assert client.headers == {
            "Content-Type": "application/json",
            "NS": "test",
            "DB": "test",
        }


@mock.patch("httpx.Client.post")
def test_query_raises_query_error(mock_post):
    """Test the query method of the SurrealDB class."""
    mock_post.return_value = mock.Mock(
        status_code=400,
        json=mock.Mock(
            return_value={
                "error": "QueryError",
                "message": "QueryError: QueryError",
            },
        ),
    )
    with SurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        with pytest.raises(QueryError):
            client.query("SELECT test")


@mock.patch("httpx.Client.post")
def test_query(mock_post):
    """Test the query method of the SurrealDB class."""
    with SurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        mock_post.return_value = MOCK_200

        assert client.query("SELECT * FROM test") == [
            {
                "id": "1",
                "name": "test",
            },
        ]


@mock.patch("httpx.Client.post")
def test_query_raises_authentication_error(mock_post):
    """Test the query method of the SurrealDB class."""
    mock_post.return_value = mock.Mock(
        status_code=403,
        json=mock.Mock(
            return_value={
                "error": "AuthenticationError",
                "message": "AuthenticationError: AuthenticationError",
            },
        ),
    )
    with SurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        with pytest.raises(AuthenticationError):
            client.query("SELECT test")


@mock.patch("httpx.Client.post")
def test_select(mock_post):
    """Test the select method of the SurrealDB class."""
    with SurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        mock_post.return_value = MOCK_200

        assert client.select("test") == [
            {
                "id": "1",
                "name": "test",
            },
        ]


@mock.patch("httpx.Client.post")
def test_create(mock_response):
    """Test the create method of the SurrealDB class."""
    with SurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        mock_response.return_value = MOCK_200

        assert client.create("test", name="test") == [
            {
                "id": "1",
                "name": "test",
            },
        ]


def test_create_raises_value_error():
    """Test the create method of the SurrealDB class."""
    with SurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        with pytest.raises(ValueError):
            client.create("test")


@mock.patch("httpx.Client.post")
def test_change(mock_response):
    """Test the change method of the SurrealDB class."""
    with SurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        mock_response.return_value = MOCK_200

        assert client.change("test:1", name="test") == [
            {
                "id": "1",
                "name": "test",
            },
        ]


def test_change_raises_value_error():
    """Test the change method of the SurrealDB class."""
    with SurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        with pytest.raises(ValueError):
            client.change("test:1")


@mock.patch("httpx.Client.post")
def test_delete(mock_post):
    """Test the delete method of the SurrealDB class."""
    with SurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        mock_post.return_value = MOCK_200

        assert client.delete("test:1") == [
            {
                "id": "1",
                "name": "test",
            },
        ]

        assert client.delete("test", where="name = test") == [
            {
                "id": "1",
                "name": "test",
            },
        ]
