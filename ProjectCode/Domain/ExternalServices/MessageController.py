from ProjectCode.Domain.ExternalServices.MessageObjects.Message import Message
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class MessageController:
    def __init__(self):
        self._read_messages = {}  # receiver_id to list of messages
        self._unread_messages = {}  # receiver_id to list of messages
        self._observers = {}    # receiver_id to observer
        self.msgCounter = 0

    def send_message(self, requester_id, receiver_id, subject, content, file=None):
        message_id = self.msgCounter
        self.msgCounter += 1
        message = Message(message_id, requester_id, receiver_id, subject, content,  file)

        if receiver_id not in self._unread_messages.keys():
            self._unread_messages[receiver_id] = []
        self._unread_messages[receiver_id].append(message)

        # Notify the observers of the new message
        # if receiver_id in self._observers:
        #     self._observers[receiver_id].raise_notifications_count()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('notifications', {
            'type': 'notify',
            'message': message,
        })

        #return message

    def read_message(self, user_id, message_id):
        for message in self._unread_messages[user_id]:
            if message.get_id() == message_id:
                message.mark_as_read()
                for observer in self._observers[user_id]:
                    observer.decrease_notifications_count()
                self._unread_messages[user_id].remove(message)  # remove from unread
                if user_id not in self._read_messages.keys():  # add to read
                    self._read_messages[user_id] = []
                self._read_messages[user_id].append(message)
                return message
        return None

    def register_observer(self, user_id, observer):
        if user_id not in self._observers.keys():
            self._observers[user_id] = []
        self._observers[user_id].append(observer)

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