from src.api.main import app


def test_app_exists() -> None:
    assert app is not None
