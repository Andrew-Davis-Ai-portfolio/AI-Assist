email_agent.py
# email_agent.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def draft_email(subject="", details="", tone="professional"):
    prompt = f"Draft a {tone} outreach email.\nSubject: {subject}\nDetails: {details}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message["content"]
