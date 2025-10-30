import os
from datetime import datetime
from typing import Dict, OrderedDict

# Optional OpenAI polish
try:
    import openai  # pip install openai
    _OPENAI = True
except Exception:
    _OPENAI = False

# ---------- template helpers ----------

def _templates_dir() -> str:
    return os.path.join(os.path.dirname(__file__), "templates")

def list_templates() -> "OrderedDict[str, str]":
    """
    Returns {filename: human_label} for every .txt in templates/.
    First non-empty line beginning with 'TITLE:' is used as label if present.
    """
    out: "OrderedDict[str, str]" = {}
    td = _templates_dir()
    if not os.path.isdir(td):
        return out
    for fname in sorted(os.listdir(td)):
        if not fname.endswith(".txt"):
            continue
        label = fname.replace("_", " ").replace(".txt", "").title()
        try:
            with open(os.path.join(td, fname), "r", encoding="utf-8") as f:
                first = f.readline().strip()
                if first.upper().startswith("TITLE:"):
                    label = first.split(":", 1)[1].strip()
        except Exception:
            pass
        out[fname] = label
    return out

def _read_template(fname: str) -> str:
    path = os.path.join(_templates_dir(), fname)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def _render(text: str, ctx: Dict[str, str]) -> Dict[str, str]:
    """
    Template format:
      TITLE: <Human friendly name>         (optional)
      SUBJECT: <subject line>              (required)
      ---                                  (required separator)
      <body with {placeholders}>
    Placeholders are Python .format(**ctx).
    """
    lines = [l.rstrip("\n") for l in text.splitlines()]
    subject = ""
    body_start = 0
    for i, ln in enumerate(lines):
        if ln.upper().startswith("SUBJECT:"):
            subject = ln.split(":", 1)[1].strip()
        if ln.strip() == "---":
            body_start = i + 1
            break
    body = "\n".join(lines[body_start:])
    # simple placeholder replacement
    subject = subject.format(**ctx)
    body = body.format(**ctx)
    return {"subject": subject, "body": body}

# ---------- AI polish (optional) ----------

def _polish_with_ai(subject: str, body: str, ctx: Dict[str, str]) -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not (_OPENAI and api_key):
        return {"subject": subject, "body": body}  # no polish available

    openai.api_key = api_key
    system = (
        "You are an assistant that rewrites email subject/body to be concise, "
        "professional, and persuasive for business outreach. Keep under 140 words."
    )
    user = (
        f"Context: {ctx}\n\n"
        f"Subject (draft): {subject}\n\n"
        f"Body (draft):\n{body}\n\n"
        "Return JSON with keys subject, body. No commentary."
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            temperature=0.4,
        )
        txt = resp["choices"][0]["message"]["content"].strip()
        # very light JSON extraction (works for our usage)
        import json, re
        json_txt = re.search(r"\{.*\}", txt, re.S)
        if json_txt:
            data = json.loads(json_txt.group(0))
            return {"subject": data.get("subject", subject),
                    "body": data.get("body", body)}
    except Exception:
        pass
    return {"subject": subject, "body": body}

# ---------- public API ----------

def generate_email(template_filename: str, context: Dict[str, str], polish_with_ai: bool = True) -> Dict[str, str]:
    """
    Renders a template with placeholders using `context`.
    Optionally polishes with OpenAI if OPENAI_API_KEY is available.
    Returns: {'subject', 'body', 'timestamp'}
    """
    raw = _read_template(template_filename)
    rendered = _render(raw, context)
    if polish_with_ai:
        rendered = _polish_with_ai(rendered["subject"], rendered["body"], context)
    rendered["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return rendered
