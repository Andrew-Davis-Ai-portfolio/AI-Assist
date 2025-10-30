# main.py
from assist_mail_ai.email_agent import print_preview

# 🔧 Edit these fields to test different outputs
ctx = {
    "subject": "Booking Inquiry — {{artist}} for {{event_city}} (Q1 Dates)",
    "recipient_name": "Taylor",
    "intro": "I’m reaching out on behalf of {{artist}} regarding upcoming slots in {{event_city}}.",
    "pitch": "High-energy 45–60 min set; strong draw with clean stage ops and fast changeover.",
    "link_1": "https://open.spotify.com/artist/xxxxx",
    "link_2": "https://www.youtube.com/watch?v=xxxxx",
    "dates": "Feb 14–18 or Mar 1–3",
    "fee": "$3,500 + travel/lodging (negotiable for multi-show route)",
    "your_name": "Andrew Davis",
    "your_role": "Artist Ops — Flame Division",
    "contact": "andrew@example.com | +1-555-555-5555",
    # extra tokens you reference inside the other fields:
    "artist": "Commander Flame",
    "event_city": "Atlanta",
}

# Optional: second pass replacement for nested placeholders (e.g., {{artist}} inside subject)
for k in list(ctx.keys()):
    for inner_k, inner_v in ctx.items():
        ctx[k] = ctx[k].replace(f"{{{{{inner_k}}}}}", str(inner_v))

print_preview(ctx)
