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


# class MessageObserver:
#     def __init__(self, user_id):
#         self._user_id = user_id
#         self._unread_count = 0
#
    # def get_user_id(self):
    #     return self._user_id
    #
    # def get_unread_count(self):
    #     return self._unread_count
    #
    # def update_unread_count(self):
    #     self._unread_count += 1
# import smtplib

# class MessageObserver:
#     def __init__(self, user_id, email):
#         self._user_id = user_id
#         self._email = email
#
#     def notify(self, message):
#         # Send an email notification to the user
#         sender = 'youremail@example.com'
#         password = 'yourpassword'
#         receiver = self._email
#         subject = 'New Message from {}'.format(message.sender_id)
#         body = 'You have received a new message: {}\n\n{}'.format(message.subject, message.content)
#         message = 'Subject: {}\n\n{}'.format(subject, body)
#
#         try:
#             server = smtplib.SMTP('smtp.gmail.com', 587)
#             server.starttls()
#             server.login(sender, password)
#             server.sendmail(sender, receiver, message)
#             print("Email notification sent to {}".format(self._email))
#         except Exception as e:
#             print("Failed to send email notification: {}".format(e))
#         finally:
#             server.quit()

class MessageObserver:
    def __init__(self, user_id):
        self.user_id = user_id
        self.notifications = 0

    def get_user_id(self):
        return self._user_id

    def get_notifications_count(self):
        return self.notifications

    def raise_notifications_count(self):
        self.notifications += 1

    def decrease_notifications_count(self):
        self.notifications -= 1

    def notify(self, message):
        self.notifications += 1
        # if the user is currently logged in, show a notification to them
        if StoreFacade().online_members.get(self.user_id):
            StoreFacade().online_members[self.user_id].show_notification(self.notifications)
        # if the user is currently offline, update their notification count in the database
        else:
            message_controller = MessageController()
            user = message_controller.get_user_by_id(self.user_id)
            user.increment_notification_count()
            message_controller.update_user(user)