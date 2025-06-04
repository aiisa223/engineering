# Autonomous Engineering Agent

This project implements a fully local engineering assistant powered by the
Ollama Gemma&nbsp;3 language model. The agent generates its own project plan,
remembers past work, executes engineering calculations, critiques the results
and finally compiles a Markdown report. Everything runs without any external
services.

## Features

- **Planner** – heuristically decomposes a high level goal into ordered tasks
  and assigns priorities.
- **MemoryManager** – keeps short‑term memory in RAM and stores long‑term
  memories on disk. A simple vector search is available to recall relevant
  items.
- **Reasoner** – interfaces with a local Ollama instance. If `ollama` is not
  installed, it falls back to an echo style response so the agent remains
  functional.
- **Executor** – contains small numerical simulations. A basic heat diffusion
  example is provided along with the ability to evaluate lightweight Python
  snippets from the LLM.
- **CritiqueEngine** – inspects execution output and notes potential issues or
  confirms the result looks reasonable.
- **DocumentCompiler** – assembles the goal, tasks and results into a
  timestamped Markdown report.

## Usage

1. Ensure Python 3.9+ is available along with `numpy` and `scipy`. Installing
   `ollama` and pulling the `gemma3` model is recommended for the reasoning
   component.
2. Run `python main.py` to launch the workflow. A Markdown report is printed to
   the console and also written to `report.md`.

Long‑term memories are stored in `memory.json` in the project directory.
