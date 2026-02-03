# CiteRAG — Grounded answers with transparent evidence
> A local research assistant that answers with evidence, not guesses.

CiteRAG is a local-first Retrieval-Augmented Generation (RAG) system for PDF-only corpora designed for research, analysis, and technical knowledge work. It enforces strict grounding: answers must be supported by retrieved document context and include citations in the form `[source.pdf:page]`.

The project aims to be privacy-respecting, reproducible, and extensible, suitable for personal knowledge bases, academic workflows, and document-heavy engineering environments.

## Core principles
- Local-first AI  
  All inference runs locally via Ollama. Your documents never leave your machine.

- Evidence-first reasoning  
  If a claim cannot be supported by retrieved context, CiteRAG avoids inventing it.

- Incremental indexing  
  Only new or changed PDFs are embedded, keeping updates fast.

- Measurable quality  
  A lightweight evaluation harness tracks citation coverage and latency.

## What CiteRAG is good for
CiteRAG works best when you need:
- Document-grounded question answering for PDF libraries
- Literature review support and technical synthesis
- Traceable answers for regulated or compliance-heavy domains
- Internal research assistants over curated corpora

CiteRAG is not intended as a general-purpose chatbot; it is designed as a research assistant that stays close to the source material.

## Tech stack
- Local LLM via Ollama (`llama3.1`)
- LangChain
- ChromaDB (vector store)
- SentenceTransformers embeddings (`sentence-transformers/all-MiniLM-L6-v2`)
- PDF parsing via `pypdf`
- Retrieval strategy: MMR (diverse top-k retrieval)

## Repository structure
├── data/              # PDFs go here 
├── src/               # Core RAG application code
├── configs/           # Configuration files (models, retrieval, prompts)
├── scripts/           # Helper scripts (indexing, utilities)
├── eval/              # Evaluation harness (latency, citation coverage)
├── docs/              # Documentation
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

## Requirements
- Python 3.13 tested (works), 3.10+ supported
- Ollama installed and running
- Supported OS: macOS, Linux, Windows

## Installation

### 1) Install Python

**macOS (Homebrew):**
```bash
brew install python
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

**Windows:**
Download and install from https://www.python.org/downloads/
During installation, enable “Add Python to PATH”.

### 2) Clone the repository
git clone https://github.com/nitro381penta/CiteRAG
cd CiteRAG

### 3) Create a virtual environment and install dependencies
macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements.txt -c constraints.txt
python3 -m pip install -e .
>>>>>>> 0af65be (Stabilize HF/Transformers deps; add constraints + pyproject; expose citerag CLI)
```

Windows (PowerShell):
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
python -m pip install -r requirements.txt -c constraints.txt
python -m pip install -e .
>>>>>>> 0af65be (Stabilize HF/Transformers deps; add constraints + pyproject; expose citerag CLI)
```

### 4) Install and pull the local model
Install Ollama from https://ollama.ai
```
ollama pull llama3.1
```

## Quickstart
1. Put PDFs into `data/`
```bash
python src/main.py
```
3. You will see an interactive prompt: "Question (or 'quit'):"
4. Example question: "What methods can we use for DNA adductomics screening?"
5. Expected output format:
	•	Answer text
	•	Sources as [pdf:page] entries
    **Question:**  
    What methods can we use for DNA adductomics screening?

    **Answer:**  
    Common approaches include LC–MS/MS, high-resolution mass spectrometry, and derivatization-based enrichment techniques, which enable detection of low-abundance DNA adducts in complex 		biological samples. [review.pdf:3] [methods.pdf:12]

## Configuration
	•	Model: llama3.1 via Ollama
	•	Embeddings: sentence-transformers/all-MiniLM-L6-v2
	•	Vector store: Chroma persisted locally
	•	Retrieval: MMR (diverse top-k)

You can override defaults via .env (optional).  
Copy .env.example to .env and adjust if needed.  
Key variables include:
- OLLAMA_MODEL (default: llama3.1)
- HF_TOKEN (optional, speeds up downloads)

## Indexing and updates
CiteRAG persists embeddings in chroma_db/. On startup it checks the data/ directory and only embeds new or modified PDFs.
To force a full rebuild, delete `chroma_db/` and rerun `citerag index`.

## Troubleshooting
	•	“ollama: command not found” → install Ollama and restart your terminal
	•	“model not found” → ollama pull llama3.1
	•	“no documents loaded” → ensure PDFs exist in data/
	•	“pip not found” (mac) → use python3 -m pip ...
    •	This error usually appears when huggingface_hub and transformers versions drift apart:
        ImportError: cannot import name 'is_offline_mode' from huggingface_hub → install over constraints:
        python -m pip install -r requirements.txt -c constraints.txt

## License
MIT 

