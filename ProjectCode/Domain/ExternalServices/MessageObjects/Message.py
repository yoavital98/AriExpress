from datetime import datetime


class Message:
    def __init__(self, message_id, sender_id, receiver_id, subject, content, creation_date, file=None):
        self._id = message_id
        self._sender_id = sender_id
        self._receiver_id = receiver_id
        self._subject = subject
        self._content = content
        self._file = file #currently not persistance
        self._date = creation_date
        self._read = False

    def get_id(self):
        return self._id

    def get_sender_id(self):
        return self._sender_id

    def get_receiver_id(self):
        return self._receiver_id

    def get_subject(self):
        return self._subject

    def get_content(self):
        return self._content

    def get_file(self):
        return self._file

    def get_date(self):
        return self._date

    def is_read(self):
        return self._read

    def mark_as_read(self):
        self._read = True

#=============JSON================
    def toJson(self):

        if self._file is None:
            file_info = None
        else:
            file_info = {
                "file": self._file
            }
            
        if self._read:
            read = "read"
        else:
            read = "pending"

        return {
            "id": self._id,
            "sender": self._sender_id,
            "receiver": self._receiver_id,
            "subject": self._subject,
            "content": self._content,
            "file": file_info,
            "creation_date": self._date,
            "status": read
        }