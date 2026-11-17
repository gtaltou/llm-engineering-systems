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