# class MessageObserver:
#     def __init__(self, user_id):
#         self._user_id = user_id
#
#     def notify(self, message):
#         # Send a real-time notification to the user that they have a new message
#         pass  # TODO: Implement notification functionality
#
#
import smtplib

class MessageObserver:
    def __init__(self, user_id, email):
        self._user_id = user_id
        self._email = email

    def notify(self, message):
        # Send an email notification to the user
        sender = 'youremail@example.com'
        password = 'yourpassword'
        receiver = self._email
        subject = 'New Message from {}'.format(message.sender_id)
        body = 'You have received a new message: {}\n\n{}'.format(message.subject, message.content)
        message = 'Subject: {}\n\n{}'.format(subject, body)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, message)
            print("Email notification sent to {}".format(self._email))
        except Exception as e:
            print("Failed to send email notification: {}".format(e))
        finally:
            server.quit()