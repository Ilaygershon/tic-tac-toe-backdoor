import smtplib
from email.message import EmailMessage


class MailSender:
    def __init__(self):
        self.first_time = True
        self.mail = "example@gmail.com"


    def message(self, url):
        title = "Your Serveo Server Link"
        body = f"""
        Hi,
        
        Here is the current link to your Flask server via Serveo:
        
        🔗 {url}
        
        You can access your app remotely through this link or share it for testing purposes.
        
        Good luck!
        """
        return body, title

    def send(self, url):
        if not self.first_time:
            return
        self.first_time = False
        body, title = self.message(url)
        try:
            msg = EmailMessage()
            msg['Subject'] = title
            msg['From'] = 'file01protect@gmail.com'
            msg['To'] = self.mail
            msg.set_content(body)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('file01protect@gmail.com', 'eyuf hpge nxhy llmw')
                smtp.send_message(msg)

        except Exception as e:
            print(f"Error sending mail:\n{e}")







