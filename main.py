import os
from dotenv import load_dotenv
from assist_mail_ai.email_agent import generate_email, list_templates

load_dotenv()

def pick_template() -> str:
    templates = list_templates()
    print("\nAvailable templates:")
    for i, (fname, label) in enumerate(templates.items(), 1):
        print(f" {i}. {label}  [{fname}]")
    choice = int(input("\nPick a template number: ").strip())
    return list(templates.keys())[choice - 1]

def gather_context(selected: str) -> dict:
    ctx = {"sender_name": "Andrew Davis"}
    if selected == "outreach_to_venue.txt":
        ctx.update({
            "recipient_name": input("Venue contact name: "),
            "artist": input("Artist name: "),
            "city": input("City: "),
            "date_window": input("Date window (e.g., Nov–Dec): "),
            "artist_primer": input("1-sentence artist primer: "),
            "draw": input("Expected draw (e.g., 200–300): "),
            "set_length": input("Set length (e.g., 45–60min): "),
            "tech": input("Tech notes (e.g., DI, 2 vocal mics): "),
            "budget": input("Budget range: "),
        })
    return ctx

def main():
    print("Assist-Mail AI (v1) — Full Upgrade Runner\n")
    selected = pick_template()
    ctx = gather_context(selected)

    result = generate_email(selected, ctx, polish_with_ai=True)
    print("\n=== SUBJECT ===")
    print(result["subject"])
    print("\n=== BODY ===")
    print(result["body"])
    print(f"\nSent via Assist-Mail AI — {result['timestamp']}")

if __name__ == "__main__":
    main()
