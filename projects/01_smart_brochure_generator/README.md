@'
# Project 01: Smart Brochure Generator

An autonomous two-stage LLM pipeline that scrapes a company's website, filters relevant subpages using **Pydantic Structured Outputs**, and streams a comprehensive Markdown brochure in real time.

## Engineering Highlights
- **Token-Efficient Scraping (`scraper.py`):** Strips DOM noise (`<script>`, `<style>`, `<svg>`, `<nav>`, `<footer>`) and normalizes URLs while using a resilient HTTP session with exponential backoff retries.
- **Agentic Link Routing (`RelevantLinks` schema):** Uses One-Shot Prompting + OpenAI Structured Outputs (`client.beta.chat.completions.parse`) at `temperature=0.0` to deterministically select high-signal subpages (About, Docs, Pricing, Careers).
- **Low-Latency Streaming:** Streams Markdown tokens in real time to the terminal via `rich.live` while enforcing context-window caps to control input token costs.
- **Multi-Provider Support:** Supports both Frontier Cloud APIs (`openai`) and Local Inference (`ollama`).

## Usage

```bash
# Default run (Hugging Face in French)
uv run projects/01_smart_brochure_generator/generator.py

# Custom company, tone, and language
uv run projects/01_smart_brochure_generator/generator.py --company "Anthropic" --url "https://www.anthropic.com" --lang "English" --tone "executive and investor-focused"

# Run locally with Ollama
uv run projects/01_smart_brochure_generator/generator.py --provider ollama
