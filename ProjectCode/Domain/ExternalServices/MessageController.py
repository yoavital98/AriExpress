from ProjectCode.Domain.ExternalServices.MessageObjects.Message import Message


class MessageController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._messages = {}
            cls._instance._observers = {}
        return cls._instance

    def send_message(self, message_id, sender_id, receiver_id, subject, content, date=None, file=None):
        if date is None:
            date = datetime.datetime.now()
        message = Message(message_id, sender_id, receiver_id, subject, content, date, file, False)
        self._messages[message_id] = message
        self.notify_observers(receiver_id, message)
        return message

    def get_all_messages_sent(self, requester_id, username):
        return [message for message in self._messages.values()
                if message.sender_id == requester_id and message.sender_id == username]

    def get_all_messages_received(self, requester_id, username):
        return [message for message in self._messages.values()
                if message.receiver_id == requester_id and message.receiver_id == username]

    def read_message(self, requester_id, message_id):
        message = self._messages.get(message_id)
        if message is None:
            return None
        if message.receiver_id != requester_id:
            return None
        message.read = True
        return message

    def register_observer(self, user_id, observer):
        if user_id not in self._observers:
            self._observers[user_id] = []
        self._observers[user_id].append(observer)

    def remove_observer(self, user_id, observer):
        if user_id in self._observers:
            self._observers[user_id].remove(observer)

    def notify_observers(self, user_id, message):
        if user_id in self._observers:
            for observer in self._observers[user_id]:
                observer.notify(message)