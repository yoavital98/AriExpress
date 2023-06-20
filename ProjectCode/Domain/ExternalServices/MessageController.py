from ProjectCode.Domain.ExternalServices.MessageObjects.Message import Message

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ProjectCode.Domain.ExternalServices.MessageObjects.Notfication import Notification
from ProjectCode.Domain.Repository.MessageRepository import MessageRepository
from ProjectCode.Domain.Repository.NotificationRepository import NotificationRepository


class MessageController:
    _instance = None

    def __new__(cls, send_notification_call=None, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            # cls._inbox_messages = {}  # message_id to message (username, list[Message])
            # cls._sent_messages = {}  # list of sent messages (username, list[Message])
            cls._inbox_messages = MessageRepository(is_receiver=True)  # message_id to message (username, list[Message])
            cls._sent_messages = MessageRepository(is_sender=True)  # list of sent messages (username, list[Message])
            cls._inbox_notifications = NotificationRepository()  # message_id to message (username, list[Notification])
            # cls.observers = []  # receiver_id to observer
            cls._msgCounter = 0
            cls._notificationCounter = 0
            cls.send_notification_call = send_notification_call #receiver_id, notification_id, type, subject:
                                                                # sendNotification(receiver_id,notification_id,type,
                                                                                                            # subject)                                                                                                       
        return cls._instance


    def send_message(self, requester_id, receiver_id, subject, content, creation_date, file=None):
        message_id = self.msgCounter
        #self.msgCounter += 1
        message = Message(message_id, requester_id, receiver_id, subject, content, creation_date, file)

        # if receiver_id not in self._inbox_messages.keys():
        #     self._inbox_messages[receiver_id] = []
        # self._inbox_messages[receiver_id].append(message)

        self._inbox_messages[receiver_id] = message

        # if requester_id not in self._sent_messages.keys():
        #     self._sent_messages[requester_id] = []
        # self._sent_messages[requester_id].append(message)

        #self._sent_messages[requester_id] = message
        self.send_notification_call(receiver_id, message_id, "message", "You got a new message: " + subject)
        return message

    def read_message(self, user_id, message_id):
        for message in self._inbox_messages[user_id]:
            if message.get_id() == int(message_id):   # changed by roobs - message_id is string
                if not message.is_read():
                    print("marking as read")
                    message.mark_as_read()
                    self._inbox_messages[user_id] = message
                return message
        return None

    def get_messages_sent(self, user_id):
        # if user_id not in self._sent_messages.keys():
        #     self._sent_messages[user_id] = []
        message_list = self._sent_messages[user_id]
        if message_list is None:
            return []
        return [message.toJson() for message in self._sent_messages[user_id]]

    def get_messages_received(self, user_id):
        # if user_id not in self._inbox_messages.keys():
        #     self._inbox_messages[user_id] = []
        message_list = self._inbox_messages[user_id]
        if message_list is None:
            return []
        return [message.toJson() for message in message_list]

    def send_notification(self, receiver_id, subject, content, creation_date):
        notification_id = self.notificationCounter
        # self.notificationCounter += 1
        message = Notification(notification_id, "AriExpress", receiver_id, subject, content, creation_date)

        # if receiver_id not in self._inbox_notifications.keys():
        #     self._inbox_notifications[receiver_id] = []
        self._inbox_notifications[receiver_id] = message
        if self.send_notification_call is not None:
            self.send_notification_call(receiver_id, notification_id, "notification", "You got a new notification: " + subject)
        return notification_id

    def read_notification(self, user_id, notification_id):
        for notification in self._inbox_notifications[user_id]:
            if notification.get_id() == int(notification_id):
                if not notification.is_read():
                    notification.mark_as_read()
                    self._inbox_notifications[user_id] = notification
                return notification
        return None

    def get_notifications(self, user_id):
        # if user_id not in self._inbox_notifications.keys():
        #     self._inbox_notifications[user_id] = []
        notification_list = self._inbox_notifications[user_id]
        if notification_list is None:
            return []
        return [message.toJson() for message in self._inbox_notifications[user_id]]

    def delete_message(self, user_id, message_id):
        for message in self._inbox_messages[user_id]:
            if message.get_id() == int(message_id):
                # self._inbox_messages[user_id].remove(message)
                self._inbox_messages.remove(message.get_id())
                return True
        return False
    
    def delete_notification(self, user_id, notification_id):
        for notification in self._inbox_notifications[user_id]:
            if notification.get_id() == int(notification_id):
                self._inbox_notifications.remove(notification.get_id())
                return True
        return False

    @property
    def msgCounter(self):
        counter = self._inbox_messages.get_highest_id()
        if counter is None:
            return 1
        return counter + 1

    @property
    def notificationCounter(self):
        counter = self._inbox_notifications.get_highest_id()
        if counter is None:
            return 1
        return counter + 1