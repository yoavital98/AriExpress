

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

        # self.notifications += 1
        # # if the user is currently logged in, show a notification to them
        # if StoreFacade().online_members.get(self.user_id):
        #     StoreFacade().online_members[self.user_id].show_notification(self.notifications)
        # # if the user is currently offline, update their notification count in the database
        # else:
        #     message_controller = MessageController()
        #     user = message_controller.get_user_by_id(self.user_id)
        #     user.increment_notification_count()
        #     message_controller.update_user(user)