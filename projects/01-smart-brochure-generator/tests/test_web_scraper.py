from src.retrieval.web_scraper import WebsiteScraper


def test_clean_html() -> None:
    html = """
    <html>
        <head>
            <title>Acme Corp</title>
        </head>
        <body>
            <nav>Menu</nav>

            <h1>Welcome</h1>

            <p>
                Acme develops innovative AI products.
            </p>

            <script>
                console.log("ignore")
            </script>
        </body>
    </html>
    """

    scraper = WebsiteScraper()

    title, content = scraper.clean_html(html)

    assert title == "Acme Corp"
    assert "Acme develops innovative AI products." in content
    assert "Menu" not in content
    
from unittest.mock import Mock
from unittest.mock import patch

from src.retrieval.web_scraper import WebsiteScraper


@patch("src.retrieval.web_scraper.requests.get")
def test_fetch_html(mock_get: Mock) -> None:
    mock_response = Mock()

    mock_response.text = "<html></html>"

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    scraper = WebsiteScraper()

    html = scraper.fetch_html("https://example.com")

    assert html == "<html></html>"

    mock_get.assert_called_once()  
    
@patch.object(
    WebsiteScraper,
    "fetch_html",
)
def test_extract(
    mock_fetch_html: Mock,
) -> None:
    mock_fetch_html.return_value = """
    <html>
        <head>
            <title>Acme</title>
        </head>
        <body>
            <main>
                We build AI software.
            </main>
        </body>
    </html>
    """

    scraper = WebsiteScraper()

    result = scraper.extract(
        "https://example.com"
    )

    assert result.url == "https://example.com"

    assert result.title == "Acme"

    assert "We build AI software." in result.content
