from src.config import settings


def test_settings_exists() -> None:
    assert settings is not None