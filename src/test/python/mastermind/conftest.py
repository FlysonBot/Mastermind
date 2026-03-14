import pytest


@pytest.fixture(scope="session", autouse=True)
def jvm():
    """Start the JVM once for the entire test session."""
    import mastermind.jvm  # noqa: F401 — importing starts the JVM as a side effect
