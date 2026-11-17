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

    NOISE_TAGS = [
        "script",
        "style",
        "nav",
        "header",
        "footer",
        "aside",
        "noscript",
        "iframe",
    ]

    def fetch_html(self, url: str) -> str:
        """Download HTML from a website."""

        response = requests.get(
            url,
            headers={"User-Agent": self.USER_AGENT},
            timeout=10,
        )

        response.raise_for_status()

        return response.text

    def remove_noise(
        self,
        soup: BeautifulSoup,
    ) -> None:
        """Remove non-content HTML elements."""

        for tag in soup(self.NOISE_TAGS):
            tag.decompose()

    def extract_main_content(
        self,
        soup: BeautifulSoup,
    ) -> str:
        """Extract the main content area."""

        main = soup.find("main")

        if main:
            return main.get_text(
                separator=" ",
                strip=True,
            )

        article = soup.find("article")

        if article:
            return article.get_text(
                separator=" ",
                strip=True,
            )

        return soup.get_text(
            separator=" ",
            strip=True,
        )

    def normalize_text(
        self,
        text: str,
    ) -> str:
        """Normalize whitespace."""

        return " ".join(text.split())

    def clean_html(
        self,
        html: str,
    ) -> tuple[str, str]:
        """Extract useful title and cleaned content."""

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        self.remove_noise(soup)

        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else "Untitled"
        )

        content = self.extract_main_content(soup)

        content = self.normalize_text(content)

        return title, content

    def extract(
        self,
        url: str,
    ) -> CompanyContent:
        """Download and process website content."""

        html = self.fetch_html(url)

        title, content = self.clean_html(html)

        return CompanyContent(
            url=url,
            title=title,
            content=content,
        )