from src.retrieval.web_scraper import WebsiteScraper


def test_main_content_extraction() -> None:
    html = """
    <html>
        <body>

            <nav>
                Home
                Pricing
                Contact
            </nav>

            <main>
                We build AI software.
            </main>

            <footer>
                Privacy Policy
            </footer>

        </body>
    </html>
    """

    scraper = WebsiteScraper()

    title, content = scraper.clean_html(html)

    assert "Home" not in content
    assert "Pricing" not in content
    assert "Privacy Policy" not in content

    assert "We build AI software." in content