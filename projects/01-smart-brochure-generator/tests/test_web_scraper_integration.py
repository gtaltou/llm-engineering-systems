import pytest

from src.retrieval.web_scraper import WebsiteScraper


@pytest.mark.integration
def test_extract_example_dot_com() -> None:
    scraper = WebsiteScraper()

    result = scraper.extract("https://example.com")

    assert result.url == "https://example.com"
    assert result.title != ""
    assert len(result.content) > 50