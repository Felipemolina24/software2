import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SenderEmail:
    def send_email(self, recipient_email, message_body, subject):
        msg = MIMEMultipart()
        # set up the parameters of the message
        password = "Auto200103"
        sender_email = "juan_fel.gomez@uao.edu.co"
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        # add in the message body
        msg.attach(MIMEText(message_body, "plain"))
        # create server
        server = smtplib.SMTP("smtp.gmail.com: 587")
        server.starttls()
        # Login Credentials for sending the mail
        server.login(sender_email, password)
        # send the message via the server.
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"successfully sent email to {recipient_email}")
