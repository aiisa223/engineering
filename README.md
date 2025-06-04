# Autonomous Engineering AI Agent (Gemma 3)

This project implements a fully local engineering assistant powered by the
Ollama Gemma 3 language model. The system plans engineering projects, carries
out numerical simulations, critiques its own output and compiles professional
reports – all without any network calls.

## Highlights

- **Recursive Planner** – breaks objectives into ordered tasks and revises the
  plan as work completes.
- **MemoryManager** – combines short term history with a FAISS vector store to
  persist knowledge across runs.
- **Reasoner** – queries a local Ollama instance. When Ollama is unavailable the
  agent continues in a safe echo mode.
- **Executor** – runs Python snippets from the model and exposes small built in
  simulations for heat diffusion and geometry problems.
- **CritiqueEngine** – performs simple self review on each result to catch
  obvious issues.
- **DocumentCompiler** – produces Markdown and optionally PDF reports using
  `pylatex` when installed.

The package only depends on local Python libraries and does not require any
cloud services.

## Getting Started

1. Install Python 3.12 and the packages in `requirements.txt`.
   A minimal setup is:

   ```bash
   pip install -r requirements.txt
   ```

   Optionally install `ollama` and pull the `gemma3` model for real LLM based
   reasoning.
2. Run the agent:

   ```bash
   python main.py
   ```

   A report will be printed to the console and saved as `report.md` in the
   project directory.

Long term memories are written to `memory.json`.
