from flask import Flask, request
import sendgrid
from sendgrid.helpers.mail import Mail
import sendgrid_config

app = Flask(__name__)
sg = sendgrid.SendGridAPIClient(api_key=sendgrid_config.SENDGRID_API_KEY)

@app.route('/', methods=['POST'])
def alertmanager_webhook():
    data = request.json

    for alert in data.get("alerts", []):
        subject = f"[{alert['labels'].get('severity').upper()}] {alert['annotations'].get('summary')}"
        message = alert['annotations'].get('description')

        email = Mail(
            from_email=sendgrid_config.FROM_EMAIL, # gets from email from sendgrid_config
            to_emails=sendgrid_config.TO_EMAIL, #gets to email from sendgrid_config
            subject=subject,
            plain_text_content=message
        )

        try:
            response = sg.send(email)
            print(f"Email sent: {subject}") 
        except Exception as e:
            print("Email failed:", e)

    return 'OK', 200

if __name__ == "__main__":
    app.run(port=5001)
