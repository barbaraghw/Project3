from twilio.rest import Client

def send_whatsapp_message(client, from_number, to_number, body_text, media_urls=None, mime_type=None):
    if media_urls is None: media_urls = []
    try:
        message = client.messages.create(from_=from_number, to=to_number,
            body=body_text, media_url=media_urls)
        print(f"WhatsApp message sent successfully. SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Error sending the WhatsApp message: {e}")
        print("Ensure your Twilio number and destination number are in the correct format (e.g., whatsapp:+1234567890).")
        print("Also verify that your Twilio credentials (Account SID and Auth Token) are correct.")
        print("If sending files, ensure they are publicly accessible via the provided URLs and served with the correct Content-Type header.")
        return False