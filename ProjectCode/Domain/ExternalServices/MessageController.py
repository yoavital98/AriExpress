from datetime import datetime
from ProjectCode.Domain.ExternalServices.MessageObjects.Message import Message
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ProjectCode.Domain.ExternalServices.MessageObjects.Notfication import Notification


def send_notification(user_id, type, message, pending_amount):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(f"{user_id}", {
        'type': type,
        'content': message,
        'unread_messages': pending_amount
    })


class MessageController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._inbox_messages = {}  # message_id to message
            cls._sent_messages = {}  # list of sent messages
            cls._inbox_notifications = {}  # message_id to message
            cls._pending_messages_amount = {}  # user_id to amount of pending messages
            cls._pending_notifications_amount = {}  # user_id to amount of pending messages
            cls.observers = []  # receiver_id to observer
            cls.msgCounter = 0
            cls.notificationCounter = 0
        return cls._instance

    def send_message(self, requester_id, receiver_id, subject, content, creation_date, file=None):
        message_id = self.msgCounter
        self.msgCounter += 1
        message = Message(message_id, requester_id, receiver_id, subject, content, creation_date, file)

        if receiver_id not in self._inbox_messages.keys():
            self._inbox_messages[receiver_id] = []
        self._inbox_messages[receiver_id].append(message)

        if receiver_id not in self._pending_messages_amount.keys():
            self._pending_messages_amount[receiver_id] = 0
        self._pending_messages_amount[receiver_id] = self._pending_messages_amount[receiver_id] + 1

        if requester_id not in self._sent_messages.keys():
            self._sent_messages[requester_id] = []
        self._sent_messages[requester_id].append(message)

        # send_notification(receiver_id, "message", "You have a new Message.", self._pending_messages_amount[receiver_id])

        return message

    def read_message(self, user_id, message_id):
        for message in self._inbox_messages[user_id]:
            if message.get_id() == int(message_id):   # changed by roobs - message_id is string
                if not message.is_read():
                    print("marking as read")
                    message.mark_as_read()
                    self._pending_messages_amount[user_id] = self._pending_messages_amount[user_id] - 1
                return message
        return None

    def get_messages_sent(self, user_id):
        if user_id not in self._sent_messages.keys():
            self._sent_messages[user_id] = []
        return [message.toJson()  for message in self._sent_messages[user_id]]

    def get_messages_received(self, user_id):
        if user_id not in self._inbox_messages.keys():
            self._inbox_messages[user_id] = []
        return [message.toJson() for message in self._inbox_messages[user_id]]

    def send_notification(self, receiver_id, subject, content, creation_date):
        message_id = self.notificationCounter
        self.notificationCounter += 1
        message = Notification(message_id, "AriExpress", receiver_id, subject, content, creation_date)

        if receiver_id not in self._inbox_notifications.keys():
            self._inbox_notifications[receiver_id] = []
        self._inbox_notifications[receiver_id].append(message)

        if receiver_id not in self._pending_notifications_amount.keys():
            self._pending_notifications_amount[receiver_id] = 0
        self._pending_notifications_amount[receiver_id] = self._pending_notifications_amount[receiver_id] + 1

        # send_notification(receiver_id, "notification", "You have a new Notification.",
        #                   self._pending_notifications_amount[receiver_id])

        return message

    def read_notification(self, user_id, message_id):
        for message in self._inbox_notifications[user_id]:
            if message.get_id() == message_id:
                if not message.is_read():
                    message.mark_as_read()
                    self._pending_notifications_amount[user_id] = self._pending_notifications_amount[user_id] - 1
                return message
        return None

    def get_notifications(self, user_id):
        if user_id not in self._inbox_notifications.keys():
            self._inbox_notifications[user_id] = []
        return [message.toJson() for message in self._inbox_notifications[user_id]]

    def delete_message(self, user_id, message_id):
        for message in self._inbox_messages[user_id]:
            if message.get_id() == int(message_id):
                self._inbox_messages[user_id].remove(message)
                if message.is_read()== False:
                    self._pending_messages_amount[user_id] = self._pending_messages_amount[user_id] - 1
                return True
        return False