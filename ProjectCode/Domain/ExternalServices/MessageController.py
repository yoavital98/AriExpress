from datetime import datetime
from ProjectCode.Domain.ExternalServices.MessageObjects.Message import Message
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_notification(user_id, message, pending_amount):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(f"{user_id}", {
        'type': 'notify',
        'message': message,
        'unread_messages': pending_amount
    })


class MessageController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._inbox_messages = {}  # message_id to message
            cls._sent_messages = {}  # list of sent messages
            cls._pending_amount = {}  # user_id to amount of pending messages
            cls.observers = []  # receiver_id to observer
            cls.msgCounter = 0
        return cls._instance

    def send_message(self, requester_id, receiver_id, subject, content, creation_date, status, file=None):
        message_id = self.msgCounter
        self.msgCounter += 1
        message = Message(message_id, requester_id, receiver_id, subject, content, creation_date, file)

        if receiver_id not in self._inbox_messages.keys():
            self._inbox_messages[receiver_id] = []
        self._inbox_messages[receiver_id].append(message)

        if receiver_id not in self._pending_amount.keys():
            self._pending_amount[receiver_id] = 0
        self._pending_amount[receiver_id] = self._pending_amount[receiver_id] + 1

        if requester_id not in self._sent_messages.keys():
            self._sent_messages[requester_id] = []
        self._sent_messages[requester_id].append(message)

        # Notify the observers
        channel_layer = get_channel_layer()

        # Send the message to the recipient's channel group
        async_to_sync(channel_layer.group_send)(
            f"user_{receiver_id}",
            {
                'type': 'message',
                'message': message.toJson(),
            }
        )

        send_notification(receiver_id, "You have a new message.", self._pending_amount[receiver_id])

        return message

    def read_message(self, user_id, message_id):
        for message in self._inbox_messages[user_id]:
            if message.get_id() == message_id:
                if not message.is_read():
                    message.mark_as_read()
                    self._pending_amount[user_id] = self._pending_amount[user_id] - 1
                return message
        return None

    def get_messages_sent(self, user_id):
        return [message for message in self._sent_messages[user_id]]

    def get_messages_received(self, user_id):
        return [message for message in self._inbox_messages[user_id]]
