"""TODO: Write a description of this module."""
from __future__ import annotations

from surreal_db import SurrealDB, Reference


def main() -> None:
    """Entry point."""
    db = SurrealDB(
        namespace="test",
        database="test",
        user=("root", "root"),
    )

    db.insert(
        table="category:education",
        name="Education",
        description="Stuff",
        cat_id=1,
    )

    db.insert(
        table="notes:test",
        title="Test",
        body="Test",
        category=Reference("category", "education"),
    )

    resp = db.select(
        "*",
        table="notes",
        where="category.name = 'Education'",
        fetch="notes, category",
    )

    print(resp)


if __name__ == "__main__":
    main()
