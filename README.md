@'
# LLM Engineering Systems

End-to-end LLM Engineering portfolio featuring 8 production-grade applications covering Multimodal APIs, Structured Outputs, Hybrid RAG pipelines, Open-Source Quantization (Hugging Face), and QLoRA Fine-Tuning.

## Architecture & Projects Roadmap

| # | Project | Core Technologies | Status |
| :--- | :--- | :--- | :--- |
| 01 | **Smart Brochure Generator** | OpenAI/Anthropic APIs, BeautifulSoup, Structured Outputs (Pydantic), Streaming | 🚧 In Progress |
| 02 | **Multimodal Customer Support Assistant** | Gradio, Whisper (Audio), Vision, Tool Calling | ⏳ Planned |
| 03 | **High-Performance Code Transpiler** | Hugging Face, vLLM, Quantization (AWQ/GGUF), Python -> C++ | ⏳ Planned |
| 04 | **Enterprise Knowledge Worker (RAG)** | LangChain/LlamaIndex, ChromaDB, Hybrid Search, Reranking | ⏳ Planned |
| 05 | **Smart Ticket Triage & Router** | Hugging Face Datasets, Embeddings, Zero-shot & Few-shot Classification | ⏳ Planned |
| 06 | **Price Predictor (Frontier Benchmarking)** | Prompt Engineering, Fine-Tuning OpenAI API, Evaluation Metrics | ⏳ Planned |
| 07 | **Price Predictor (Open-Source QLoRA)** | PEFT, LoRA/QLoRA, bitsandbytes, SFTTrainer, Weights & Biases | ⏳ Planned |
| 08 | **Autonomous Deal Finder System** | RAG + Fine-Tuned Model + Agentic Workflow + Push Notifications | ⏳ Planned |

## Tech Stack & Tooling
- **Package & Environment Manager:** `uv`
- **Python Version:** 3.12
- **Models:** OpenAI (GPT-4o), Anthropic (Claude 3.5 Sonnet), Meta (Llama 3), Mistral, Qwen

## Local Setup

```bash
git clone https://github.com/gtaltou/llm-engineering-systems.git
cd llm-engineering-systems
uv sync
cp .env.example .env
