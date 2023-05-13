import datetime

class Message:
    def __init__(self, message_id, sender_id, receiver_id, subject, content, date, file, read):
        self.message_id = message_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.subject = subject
        self.content = content
        self.date = date
        self.file = file
        self.read = read