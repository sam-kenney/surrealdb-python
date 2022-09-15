"""Module for referencing data across SurrealDB tables."""
from __future__ import annotations
import typing


class Reference:
    """Reference to another SurrealDB table."""

    def __init__(self, table: str, record_id: typing.Any):
        """
        # SurrealDB Reference.

        Create a reference to another table.

        Params:
            table: str
                The name of the table to reference.

            record_id: Any
                The id of the record to reference from that table.
        """
        self.table = table
        self.record_id = record_id

    def __format__(self, format_spec: str) -> str:
        """Format the reference as a string."""
        if format_spec:
            raise NotImplementedError("Format specifiers are not supported.")

        return f"{self.table}:{self.record_id}"
