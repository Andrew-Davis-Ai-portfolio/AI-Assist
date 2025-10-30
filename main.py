from assist_mail_ai.email_agent import print_preview

def main():
    print("Assist-Mail AI — Preview Mode 📨")
    print("----------------------------------")
    
    sender = input("Your Name: ")
    recipient = input("Recipient Name: ")
    company = input("Company Name: ")
    offer = input("Offer / Purpose: ")

    ctx = {
        "sender_name": sender,
        "recipient_name": recipient,
        "company": company,
        "offer": offer,
    }

    print_preview(ctx)

if __name__ == "__main__":
    main()
