"""Module to manage a SurrealDB database."""
from __future__ import annotations
from typing import Any, Dict, Tuple

import httpx


class SurrealDB:
    """TODO: Write a description of this class."""

    def __init__(
        self,
        namespace: str,
        database: str,
        user: Tuple[str, str],
        domain: str = "http://localhost:8000",
    ) -> SurrealDB:
        """TODO: Write a description of this method."""
        headers = {
            "Content-Type": "application/json",
            "NS": namespace,
            "DB": database,
        }
        self.__client = httpx.Client(auth=user, headers=headers)
        self.url = f"{domain}/sql"

    def select(
        self,
        *args,
        table: str,
        where: str = None,
        fetch: str = None,
    ) -> Dict[str, Any]:
        """TODO: Write a description of this method."""
        query = f"SELECT {', '.join(args)} FROM {table}"
        if where:
            query += f" WHERE {where}"
        if fetch:
            query += f" FETCH {fetch}"

        response = self.__client.post(url=self.url, data=query)

        if response.status_code == 200:
            return response.json()[0]

        raise Exception(response.text)

    @staticmethod
    def __generate_create_statement(table: str, **kwargs) -> str:
        """Return a SurrealDB syntax create statement."""
        if not kwargs:
            raise ValueError("Must set at least one value.")

        query = f"CREATE {table} SET "

        for key, value in kwargs.items():
            if isinstance(value, str):
                value = f"'{value}'"
            query += f"{key} = {value}, "

        return query[:-2] + ";"

    def insert(self, table: str, **kwargs) -> Dict[str, Any]:
        """TODO: Write a description of this method."""
        query = self.__generate_create_statement(table, **kwargs)
        response = self.__client.post(url=self.url, data=query)

        if response.status_code == 200:
            return response.json()[0]

        raise Exception(response.text)
