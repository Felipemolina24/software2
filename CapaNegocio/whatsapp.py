from twilio.rest import Client


class WhatsAppSender:
    def __init__(self):
        self.account_sid = "AC39c0d5426ff0036526e45018c7de846a"  # Reemplaza con tu Account SID de Twilio
        self.auth_token = (
            "d69e5aa03e9d3285bf59bf75f08e0b35"  # Reemplaza con tu Auth Token de Twilio
        )
        self.client = Client(self.account_sid, self.auth_token)
        self.from_whatsapp_number = (
            "whatsapp:+14155238886"  # Número de WhatsApp de Twilio
        )

    def send_whatsapp_message(self, to, message):
        message = self.client.messages.create(
            body=message, from_=self.from_whatsapp_number, to=f"whatsapp:{to}"
        )
        print(f"Message sent to {to}. Message SID: {message.sid}")
