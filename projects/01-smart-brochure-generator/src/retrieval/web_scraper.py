from __future__ import annotations

import requests
from bs4 import BeautifulSoup

from src.schemas.company_content import CompanyContent


class WebsiteScraper:
    """Website content extraction utility."""

    USER_AGENT = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/131.0.0.0 "
        "Safari/537.36"
    )

    def fetch_html(self, url: str) -> str:
        """Download HTML from a website."""

        response = requests.get(
            url,
            headers={"User-Agent": self.USER_AGENT},
            timeout=10,
        )

        response.raise_for_status()

        return response.text

    def clean_html(self, html: str) -> tuple[str, str]:
        """Extract useful title and visible text."""

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "header",
                "footer",
                "noscript",
                "iframe",
            ]
        ):
            tag.decompose()

        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else "Untitled"
        )

        text = soup.get_text(separator=" ", strip=True)

        content = " ".join(text.split())

        return title, content

    def extract(self, url: str) -> CompanyContent:
        """Download and process website content."""

        html = self.fetch_html(url)

        title, content = self.clean_html(html)

        return CompanyContent(
            url=url,
            title=title,
            content=content,
        )
