import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def _create_resilient_session() -> requests.Session:
    """Creates an HTTP session with connection pooling and exponential backoff retries."""
    session = requests.Session()
    session.headers.update(HEADERS)
    retry_strategy = Retry(
        total=3,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

SESSION = _create_resilient_session()


class WebsiteScraper:
    """Scrapes a webpage with resilient retries, cleans HTML noise to save LLM tokens, and extracts links."""

    def __init__(self, url: str, polite_delay: float = 0.5):
        self.url = url.rstrip("/")
        self.title = ""
        self.text = ""
        self.links: list[str] = []
        if polite_delay > 0:
            time.sleep(polite_delay)
        self._scrape()

    def _scrape(self) -> None:
        response = SESSION.get(self.url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        self.title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"

        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input", "svg", "noscript", "footer", "nav"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)

        raw_links = [link.get("href") for link in soup.find_all("a") if link.get("href")]
        normalized = {
            urljoin(self.url + "/", href).split("#")[0].rstrip("/")
            for href in raw_links
            if href.startswith(("http", "/"))
        }
        # Exclude the landing page URL itself to avoid duplicate scraping
        self.links = sorted(link for link in normalized if link != self.url)

    def get_contents(self, max_chars: int = 4000) -> str:
        return f"Webpage Title: {self.title}\nWebpage URL: {self.url}\nWebpage Contents:\n{self.text[:max_chars]}\n"
