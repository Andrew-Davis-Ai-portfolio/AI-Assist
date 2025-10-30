import os
import openai
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_email(recipient_name, company, offer, sender_name="Andrew Davis"):
    prompt = f"""
    Write a professional outreach email:

    To: {recipient_name} at {company}
    Offer: {offer}
    From: {sender_name}

    Tone: Confident, clear, business professional  
    Keep it under 160 words.  
    Include a strong call-to-action.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a business email writing assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7
    )

    message = response["choices"][0]["message"]["content"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    return f"{message}\n\nSent via Assist-Mail AI — {timestamp}"
