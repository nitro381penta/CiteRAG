import subprocess
import sys
import typer

app = typer.Typer(add_completion=False, help="CiteRAG CLI")

def _run(cmd: list[str]) -> None:
    subprocess.run([sys.executable, *cmd], check=True)

@app.command()
def index():
    """Build/update the local Chroma index from PDFs in data/."""
    _run(["scripts/index.py"])

@app.command()
def chat():
    """Interactive chat with citations."""
    _run(["scripts/chat.py"])

@app.command()
def eval():
    """Run the tiny evaluation harness."""
    _run(["scripts/eval.py"])
