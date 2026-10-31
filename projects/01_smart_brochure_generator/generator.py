import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

from scraper import WebsiteScraper

load_dotenv(override=True)


class LinkItem(BaseModel):
    type: str = Field(description="Category of the page, e.g., 'about page', 'careers page', 'pricing page', 'docs'")
    url: str = Field(description="Full absolute URL of the relevant page")


class RelevantLinks(BaseModel):
    links: list[LinkItem] = Field(description="List of links relevant for a company brochure")


class BrochureGenerator:
    """End-to-end LLM pipeline: Web Scraping -> Structured Link Routing -> Streaming Markdown Generation."""

    def __init__(self, provider: str = "openai", model_filter: str = "gpt-4o-mini", model_writer: str = "gpt-4o-mini"):
        self.console = Console()
        self.provider = provider.lower()

        if self.provider == "ollama":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            self.client = OpenAI(base_url=base_url, api_key="ollama")
            self.model_filter = model_filter if model_filter != "gpt-4o-mini" else "llama3.2"
            self.model_writer = model_writer if model_writer != "gpt-4o-mini" else "llama3.2"
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key or api_key.startswith("sk-proj-..."):
                raise ValueError("OPENAI_API_KEY is missing or invalid in your .env file.")
            self.client = OpenAI(api_key=api_key)
            self.model_filter = model_filter
            self.model_writer = model_writer

    def select_relevant_links(self, site: WebsiteScraper) -> RelevantLinks:
        """Uses LLM Structured Outputs + One-Shot Prompting to filter relevant URLs."""
        system_prompt = (
            "You are an intelligent web router. You are provided with a list of links found on a webpage. "
            "Decide which of the links would be most relevant to include in a brochure about the company, "
            "such as links to an About page, Company page, Products/Services, Docs, Pricing, or Careers/Jobs pages.\n"
            "Do NOT include the root homepage URL itself. Ignore Terms of Service, Privacy Policies, Login pages, and social media links.\n"
            "Example output format:\n"
            '{"links": [{"type": "about page", "url": "https://example.com/about"}, '
            '{"type": "careers page", "url": "https://example.com/careers"}]}'
        )

        user_prompt = (
            f"Here is the list of links on the website of {site.url}.\n"
            "Please select up to 4 most relevant distinct links for a company brochure:\n"
            + "\n".join(site.links[:80])
        )

        response = self.client.beta.chat.completions.parse(
            model=self.model_filter,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=RelevantLinks,
            temperature=0.0,
        )
        return response.choices[0].message.parsed

    def assemble_context(self, url: str) -> str:
        """Scrapes the landing page + LLM-selected subpages into a clean context window."""
        self.console.print(f"[bold cyan]1. Scraping landing page:[/bold cyan] {url}")
        main_site = WebsiteScraper(url, polite_delay=0.0)
        context = f"## Landing Page\n{main_site.get_contents()}"

        self.console.print(
            f"[bold cyan]2. Filtering {len(main_site.links)} links using {self.model_filter} (Structured Outputs)...[/bold cyan]"
        )
        relevant = self.select_relevant_links(main_site)

        visited = {main_site.url}
        for item in relevant.links:
            clean_url = item.url.rstrip("/")
            if clean_url in visited or len(visited) >= 5:
                continue
            visited.add(clean_url)

            self.console.print(f"   [green]→ Fetching {item.type}:[/green] {clean_url}")
            try:
                sub_site = WebsiteScraper(clean_url, polite_delay=0.6)
                context += f"\n\n## Subpage ({item.type})\n{sub_site.get_contents(max_chars=2500)}"
            except Exception as e:
                self.console.print(f"   [yellow]⚠ Skipped {clean_url}: {e}[/yellow]")

        return context[:16000]

    def stream_brochure(
        self, company_name: str, url: str, tone: str = "professionnel, analytique et orienté ingénierie", language: str = "Français"
    ) -> str:
        """Streams the generated brochure in real-time Markdown."""
        context = self.assemble_context(url)

        system_prompt = (
            f"You are an expert technical copywriter and AI consultant. You analyze the contents of several relevant pages "
            f"from a company's website and create a comprehensive, well-structured brochure about the company for prospective "
            f"customers, investors, and recruits. Write in {language} with a {tone} tone. "
            f"Include clear Markdown sections for: Executive Summary / Value Proposition, Core Products & Architecture, "
            f"Target Audience & Use Cases, and Company Culture / Careers."
        )

        user_prompt = (
            f"Company Name: {company_name}\n"
            f"Website URL: {url}\n"
            f"Here are the contents of its landing page and key subpages; use this factual information to build the brochure:\n\n"
            f"{context}"
        )

        self.console.print(f"\n[bold magenta]3. Streaming Brochure for {company_name} ({self.model_writer})...[/bold magenta]\n")

        stream = self.client.chat.completions.create(
            model=self.model_writer,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=True,
            temperature=0.3,
        )

        full_response = ""
        with Live(Markdown(""), refresh_per_second=10, console=self.console) as live:
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                live.update(Markdown(full_response))

        return full_response


def main():
    parser = argparse.ArgumentParser(description="AI-Powered Smart Company Brochure Generator")
    parser.add_argument("--company", type=str, default="Hugging Face", help="Company name")
    parser.add_argument("--url", type=str, default="https://huggingface.co", help="Company landing page URL")
    parser.add_argument("--tone", type=str, default="professionnel, analytique et orienté ingénierie", help="Writing tone")
    parser.add_argument("--lang", type=str, default="Français", help="Output language")
    parser.add_argument("--provider", type=str, choices=["openai", "ollama"], default="openai", help="LLM Provider")
    parser.add_argument("--output", type=str, default="projects/01_smart_brochure_generator/sample_brochure.md", help="Output Markdown path")
    args = parser.parse_args()

    generator = BrochureGenerator(provider=args.provider)
    brochure_md = generator.stream_brochure(
        company_name=args.company,
        url=args.url,
        tone=args.tone,
        language=args.lang,
    )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(brochure_md)
    print(f"\nBrochure sauvegardée dans : {args.output}")


if __name__ == "__main__":
    main()
