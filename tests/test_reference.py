"""Test the Reference class."""
from __future__ import annotations

import pytest

from surrealdb import Reference


def test_reference_format():
    """Test the format method of the Reference class."""
    reference = Reference("table", "record_id")
    assert f"{reference}" == "table:record_id"

    with pytest.raises(NotImplementedError):
        f"{reference:''}"
