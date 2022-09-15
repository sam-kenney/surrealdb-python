"""Nox configuration to Lint, Format and Test code."""
import os

import nox


@nox.session
def reformat(session):
    """Reformat using Black."""
    session.install("black")
    session.run("black", ".")


@nox.session
def lint(session):
    """Lint using Flake8."""
    session.install(
        "flake8",
        "flake8-docstrings",
        "flake8-import-order",
        "nox",
    )
    if os.path.isfile("requirements.txt"):
        session.install("-r", "requirements.txt")

    session.run("flake8", "--max-complexity=8")


@nox.session
def test(session):
    """Run unit tests using Pytest Coverage."""
    session.install("pytest", "pytest-cov")
    session.install("-r", "requirements.txt")
    session.run("pytest", "--cov")


@nox.session
def lintsql(session):
    """Lint SQL models using SQLFluff."""
    if os.path.isdir("models"):
        session.install("sqlfluff")
        session.run("sqlfluff", "lint", "models")
