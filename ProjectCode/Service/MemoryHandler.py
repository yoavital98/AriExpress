import logging


class MemoryHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.messages = []

    def emit(self, record):
        self.messages.append(self.format(record))

    def get_messages(self):
        return self.messages
