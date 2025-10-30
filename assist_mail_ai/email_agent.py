# assist_mail_ai/email_agent.py
from pathlib import Path
from typing import Dict, Tuple

TEMPLATE_FILE = Path(__file__).with_name("templates") / "default_email.txt"

def load_template() -> str:
    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(f"Template not found at {TEMPLATE_FILE}")
    return TEMPLATE_FILE.read_text(encoding="utf-8")

def render(text: str, ctx: Dict[str, str]) -> str:
    # Simple {{placeholder}} replacement; leaves unknown placeholders as-is
    out = text
    for k, v in ctx.items():
        out = out.replace(f"{{{{{k}}}}}", str(v))
    return out

def preview_email(ctx: Dict[str, str]) -> Tuple[str, str]:
    """
    Renders the template and returns (subject, body) WITHOUT sending.
    Subject is the first line if it starts with 'Subject:'; otherwise blank.
    """
    raw = render(load_template(), ctx)
    lines = raw.splitlines()
    subject = ""
    if lines and lines[0].strip().lower().startswith("subject:"):
        subject = lines[0].split(":", 1)[1].strip()
        body = "\n".join(lines[1:]).lstrip("\n")
    else:
        body = raw
    return subject, body

def print_preview(ctx: Dict[str, str]) -> None:
    subject, body = preview_email(ctx)
    print("=" * 72)
    print(f"SUBJECT: {subject}")
    print("-" * 72)
    print(body)
    print("=" * 72)
