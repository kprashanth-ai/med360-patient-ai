"""
Reads the codebase and generates/updates three Obsidian docs:
  docs/API_REFERENCE.md   — all endpoints, request/response schemas
  docs/MODULES.md         — each module's purpose, functions, dependencies
  docs/DATA_MODELS.md     — all Pydantic models and their fields

Run manually:  python scripts/update_docs.py
Auto-run:      git pre-push hook + Claude Code stop hook
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
APP  = ROOT / "app"

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# ── file collection ────────────────────────────────────────────────────────────

GROUPS = {
    "api":     ["app/api/v1/", "app/main.py"],
    "modules": ["app/modules/", "app/services/", "app/prompts/", "app/tracker.py"],
    "models":  [
        "app/modules/recommender/engine.py",
        "app/modules/report_interpreter/engine.py",
        "app/modules/chatbot/engine.py",
    ],
}


def collect_files(paths: list[str]) -> dict[str, str]:
    files = {}
    for p in paths:
        target = ROOT / p
        if target.is_file():
            files[p] = target.read_text(encoding="utf-8")
        elif target.is_dir():
            for f in sorted(target.rglob("*.py")):
                if f.stat().st_size > 0 and "__init__" not in f.name:
                    key = str(f.relative_to(ROOT)).replace("\\", "/")
                    files[key] = f.read_text(encoding="utf-8")
    return files


def format_sources(files: dict[str, str]) -> str:
    parts = []
    for path, content in files.items():
        parts.append(f"### {path}\n```python\n{content}\n```")
    return "\n\n".join(parts)


# ── generators ─────────────────────────────────────────────────────────────────

async def generate(system: str, sources: str, doc_name: str) -> str:
    print(f"  Generating {doc_name}...")
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": sources},
        ],
    )
    return response.choices[0].message.content


API_PROMPT = """
You are a technical documentation writer producing industry-standard API reference docs.

Given FastAPI route files and Pydantic schemas, write a clean Markdown API reference with:
- A brief intro section (what this API does, base URL pattern)
- One section per endpoint:
  - Method + path as heading
  - Description (what it does, when to use it)
  - Request body (table: field, type, required, description)
  - Response body (table: field, type, description)
  - Example request (curl)
  - Example response (JSON)
- A section listing all error responses

Format: clean GitHub-flavoured Markdown. Use tables, code blocks. Be precise and concise.
Start with: # API Reference
""".strip()

MODULES_PROMPT = """
You are a technical documentation writer producing industry-standard module/architecture docs.

Given Python source files for services, modules, core logic, and prompts, write a Markdown document with:
- A brief architecture overview (how the modules connect)
- One section per module/service:
  - Purpose (one sentence)
  - Key functions/classes with signatures and what they do
  - Inputs and outputs
  - Dependencies (what it imports from other modules)
  - Usage example (short code snippet if useful)
- A data flow section showing how a patient request flows through the system

Format: clean GitHub-flavoured Markdown. Use headings, bullet points, code blocks.
Start with: # Module Reference
""".strip()

MODELS_PROMPT = """
You are a technical documentation writer producing industry-standard data model docs.

Given Pydantic model and schema files, write a Markdown document with:
- A brief intro (what these models represent, JSON file storage note)
- One section per model:
  - Purpose (one sentence)
  - Fields table: field name | type | required | default | description
  - Example JSON instance
- A section on how models relate to each other

Format: clean GitHub-flavoured Markdown. Use tables, code blocks.
Start with: # Data Models
""".strip()


# ── writer ─────────────────────────────────────────────────────────────────────

_FRONTMATTER = {
    "API_REFERENCE.md": "tags: [api, reference, auto-generated]",
    "MODULES.md":       "tags: [modules, reference, auto-generated]",
    "DATA_MODELS.md":   "tags: [models, reference, auto-generated]",
}


def write_doc(filename: str, content: str):
    path = DOCS / filename
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    fm = _FRONTMATTER.get(filename, "")
    frontmatter = f"---\n{fm}\nupdated: \"{timestamp}\"\n---\n\n" if fm else ""
    header = f"> Auto-generated on {timestamp} by `scripts/update_docs.py`. Do not edit manually.\n\n"
    path.write_text(frontmatter + header + content, encoding="utf-8")
    print(f"  Written -> docs/{filename}")


# ── main ───────────────────────────────────────────────────────────────────────

async def main():
    DOCS.mkdir(exist_ok=True)
    print(f"\nMed360 Docs Generator")
    print("=" * 40)

    tasks = [
        generate(API_PROMPT,     format_sources(collect_files(GROUPS["api"])),     "API_REFERENCE.md"),
        generate(MODULES_PROMPT, format_sources(collect_files(GROUPS["modules"])), "MODULES.md"),
        generate(MODELS_PROMPT,  format_sources(collect_files(GROUPS["models"])),  "DATA_MODELS.md"),
    ]

    results = await asyncio.gather(*tasks)

    write_doc("API_REFERENCE.md", results[0])
    write_doc("MODULES.md",       results[1])
    write_doc("DATA_MODELS.md",   results[2])

    print("\nDone. All docs updated in docs/\n")


if __name__ == "__main__":
    asyncio.run(main())
