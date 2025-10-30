import os
import openai
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_email(recipient_name, company, offer, sender_name):
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
            {"role": "system", "content": "You are a professional outreach assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    email_text = response.choices[0].message.content.strip()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return {
        "timestamp": timestamp,
        "subject": f"Opportunity: {offer}",
        "email": email_text
    }


if __name__ == "__main__":
    recipient = input("Recipient name: ")
    company = input("Company: ")
    offer = input("Offer details: ")
    sender = input("Your name: ")

    result = generate_email(recipient, company, offer, sender)

    print("\n----- EMAIL GENERATED -----")
    print(f"Time: {result['timestamp']}")
    print(f"Subject: {result['subject']}\n")
    print(f"{result['email']}")
