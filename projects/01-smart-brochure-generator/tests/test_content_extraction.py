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

    _, content = scraper.clean_html(html)

    assert "Home" not in content
    assert "Pricing" not in content
    assert "Privacy Policy" not in content
    assert "We build AI software." in content


def test_clean_html_without_title() -> None:
    html = """
    <html>
        <body>
            <main>Hello world</main>
        </body>
    </html>
    """

    scraper = WebsiteScraper()

    title, content = scraper.clean_html(html)

    assert title == "Untitled"
    assert content == "Hello world"


def test_extract_article_content() -> None:
    html = """
    <html>
        <body>
            <article>
                Article content
            </article>
        </body>
    </html>
    """

    scraper = WebsiteScraper()

    _, content = scraper.clean_html(html)

    assert "Article content" in content


def test_extract_body_fallback() -> None:
    html = """
    <html>
        <body>
            Generic content
        </body>
    </html>
    """

    scraper = WebsiteScraper()

    _, content = scraper.clean_html(html)

    assert "Generic content" in content


def test_remove_script_content() -> None:
    html = """
    <html>
        <body>
            <script>alert('test')</script>
            <main>Important content</main>
        </body>
    </html>
    """

    scraper = WebsiteScraper()

    _, content = scraper.clean_html(html)

    assert "alert" not in content
    assert "Important content" in content