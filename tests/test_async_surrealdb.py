"""Test the AsyncSurrealDB class."""
from __future__ import annotations
from unittest import mock

import pytest

from surrealdb import AuthenticationError, QueryError, AsyncSurrealDB


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
    """Test the headers of the AsyncSurrealDB class."""
    client = AsyncSurrealDB(
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


@pytest.mark.asyncio
async def test_signin():
    """Test the signin method of the AsyncSurrealDB class."""
    async with AsyncSurrealDB() as client:
        await client.signin("admin", "admin")


@pytest.mark.asyncio
async def test_signup():
    """Test the signup method of the AsyncSurrealDB class."""
    async with AsyncSurrealDB() as client:
        await client.signup("admin", "admin")


@pytest.mark.asyncio
async def test_use():
    """Test the use method of the AsyncSurrealDB class."""
    async with AsyncSurrealDB() as client:
        await client.use("test", "test")

        assert client.headers == {
            "Content-Type": "application/json",
            "NS": "test",
            "DB": "test",
        }


@mock.patch("httpx.AsyncClient.post")
@pytest.mark.asyncio
async def test_query_raises_query_error(mock_post):
    """Test the query method of the AsyncSurrealDB class."""
    mock_post.return_value = mock.Mock(
        status_code=400,
        json=mock.Mock(
            return_value={
                "error": "QueryError",
                "message": "QueryError: QueryError",
            },
        ),
    )
    async with AsyncSurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        with pytest.raises(QueryError):
            await client.query("SELECT test")


@mock.patch("httpx.AsyncClient.post")
@pytest.mark.asyncio
async def test_query(mock_post):
    """Test the query method of the AsyncSurrealDB class."""
    async with AsyncSurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        mock_post.return_value = MOCK_200

        assert await client.query("SELECT * FROM test") == [
            {
                "id": "1",
                "name": "test",
            },
        ]


@mock.patch("httpx.AsyncClient.post")
@pytest.mark.asyncio
async def test_query_raises_authentication_error(mock_post):
    """Test the query method of the AsyncSurrealDB class."""
    mock_post.return_value = mock.Mock(
        status_code=403,
        json=mock.Mock(
            return_value={
                "error": "AuthenticationError",
                "message": "AuthenticationError: AuthenticationError",
            },
        ),
    )
    async with AsyncSurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        with pytest.raises(AuthenticationError):
            await client.query("SELECT test")


@mock.patch("httpx.AsyncClient.post")
@pytest.mark.asyncio
async def test_select(mock_post):
    """Test the select method of the AsyncSurrealDB class."""
    async with AsyncSurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        mock_post.return_value = MOCK_200

        assert await client.select("test") == [
            {
                "id": "1",
                "name": "test",
            },
        ]


@mock.patch("httpx.AsyncClient.post")
@pytest.mark.asyncio
async def test_create(mock_response):
    """Test the create method of the AsyncSurrealDB class."""
    async with AsyncSurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        mock_response.return_value = MOCK_200

        assert await client.create("test", name="test") == [
            {
                "id": "1",
                "name": "test",
            },
        ]


@pytest.mark.asyncio
async def test_create_raises_value_error():
    """Test the create method of the AsyncSurrealDB class."""
    async with AsyncSurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        with pytest.raises(ValueError):
            await client.create("test")


@mock.patch("httpx.AsyncClient.post")
@pytest.mark.asyncio
async def test_change(mock_response):
    """Test the change method of the AsyncSurrealDB class."""
    async with AsyncSurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        mock_response.return_value = MOCK_200

        assert await client.change("test:1", name="test") == [
            {
                "id": "1",
                "name": "test",
            },
        ]


@pytest.mark.asyncio
async def test_change_raises_value_error():
    """Test the change method of the AsyncSurrealDB class."""
    async with AsyncSurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        with pytest.raises(ValueError):
            await client.change("test:1")


@mock.patch("httpx.AsyncClient.post")
@pytest.mark.asyncio
async def test_delete(mock_post):
    """Test the delete method of the AsyncSurrealDB class."""
    async with AsyncSurrealDB(
        username="admin",
        password="admin",
        namespace="test",
        database="test",
        url="http://localhost:8000/sql",
    ) as client:
        mock_post.return_value = MOCK_200

        assert await client.delete("test:1") == [
            {
                "id": "1",
                "name": "test",
            },
        ]

        assert await client.delete("test", where="name = test") == [
            {
                "id": "1",
                "name": "test",
            },
        ]
