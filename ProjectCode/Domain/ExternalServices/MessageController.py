from datetime import datetime
from ProjectCode.Domain.ExternalServices.MessageObjects.Message import Message
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



def send_notification(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(f"user_{user_id}", {
        'type': 'notify',
        'message': message,
    })

class MessageController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._read_messages = {}  # receiver_id to list of messages
            cls._unread_messages = {}  # receiver_id to list of messages
            cls.observers = []  # receiver_id to observer
            cls.msgCounter = 0
        return cls._instance
    #
    # def attach(self, observer):
    #     self.observers.append(observer)
    #
    # def detach(self, observer):
    #     self.observers.remove(observer)
    #
    # def notify_observers(self, message):
    #     for observer in self.observers:
    #         observer.update(message)

    def send_message(self, requester_id, receiver_id, subject, content, creation_date, status, file=None):
        message_id = self.msgCounter
        self.msgCounter += 1
        message = Message(message_id, requester_id, receiver_id, subject, content, creation_date, file)

        if receiver_id not in self._unread_messages.keys():
            self._unread_messages[receiver_id] = []
        self._unread_messages[receiver_id].append(message)

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

        send_notification(receiver_id, "You have a new message")

        return message

    def read_message(self, user_id, message_id):
        for message in self._unread_messages[user_id]:
            if message.get_id() == message_id:
                message.mark_as_read()
                for observer in self.observers[user_id]:
                    observer.decrease_notifications_count()
                self._unread_messages[user_id].remove(message)  # remove from unread
                if user_id not in self._read_messages.keys():  # add to read
                    self._read_messages[user_id] = []
                self._read_messages[user_id].append(message)
                return message
        return None

    def register_observer(self, user_id, observer):
        if user_id not in self.observers.keys():
            self.observers[user_id] = []
        self.observers[user_id].append(observer)

    def get_messages_sent(self, user_id):
        return [message for message in self._messages if message.get_sender_id() == user_id]

    def get_messages_received(self, user_id):
        messages = [message for message in self._messages if message.get_receiver_id() == user_id]
        for message in messages:
            if not message.is_read():
                message.mark_as_read()
                for observer in self._observers[user_id]:
                    observer.update_unread_count()
        return messages

