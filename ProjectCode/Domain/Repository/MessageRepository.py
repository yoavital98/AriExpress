from peewee import fn

from ProjectCode.DAL.MessageModel import MessageModel
from ProjectCode.Domain.ExternalServices.MessageObjects.Message import Message
from ProjectCode.Domain.Repository.Repository import Repository


class MessageRepository(Repository):

    def __init__(self, is_sender=False, is_receiver=False):
        self.is_sender = is_sender
        self.is_receiver = is_receiver
        self.model = MessageModel

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("MessageRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("MessageRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
        try:
            return self.contains(item)
        except Exception as e:
            return False

    def get(self, pk=None):
        if self.is_sender:
            return self.get_sender_messages(pk)
        elif self.is_receiver:
            return self.get_receiver_messages(pk)
        else:
            raise "MessageRepository: get: is_sender and is_receiver are both False"

    def get_sender_messages(self, pk):
        try:
            if pk is None:
                query = MessageModel.select().order_by(MessageModel.sender_id)
                message_lists = self.__createMessageLists(query, "sender_id")
                return message_lists
            else:
                message_list = []
                message_entry = MessageModel.select().where(MessageModel.sender_id == pk)
                for message in message_entry:
                    message_list.append(self.__createDomainObject(message))
                return message_list
        except Exception as e:
            return []

    def get_receiver_messages(self, pk):
        try:
            if pk is None:
                query = MessageModel.select().order_by(MessageModel.receiver_id)
                message_lists = self.__createMessageLists(query, "receiver_id")
                return message_lists
            else:
                message_list = list()
                message_entry = MessageModel.select().where(MessageModel.receiver_id == pk)
                for message in message_entry:
                    message_list.append(self.__createDomainObject(message))
                return message_list
        except Exception as e:
            return []

    def __createMessageLists(self, query, field_name):
        message_lists = []
        cur_username = getattr(query[0], field_name)
        cur_list = []
        for message in query:
            message_username = getattr(message, field_name)
            if cur_username == message_username:
                cur_list.append(self.__createDomainObject(message))
            else:
                message_lists.append(cur_list)
                cur_list = []
                cur_username = message_username
                cur_list.append(self.__createDomainObject(message))
        message_lists.append(cur_list)
        return message_lists

    def __createDomainObject(self, message_entry):
        message_dom = Message(message_entry.message_id, message_entry.sender_id, message_entry.receiver_id, message_entry.subject, message_entry.content, message_entry.date)
        if message_entry.read:
            message_dom.mark_as_read()
        return message_dom

    def add(self, message):
        message_entry = self.model.get_or_none(self.model.message_id == message.get_id())
        if message_entry is not None:
            #update
            message_entry.sender_id = message.get_sender_id()
            message_entry.receiver_id = message.get_receiver_id()
            message_entry.subject = message.get_subject()
            message_entry.content = message.get_content()
            message_entry.date = message.get_date()
            message_entry.read = message.is_read()
            message_entry.save()
            return message
        MessageModel.create(sender_id=message.get_sender_id(), receiver_id=message.get_receiver_id(), subject=message.get_subject(), content=message.get_content(), date=message.get_date())
        return message

    def remove(self, pk):
        message_entry = self.model.get(self.model.message_id == pk)
        message_entry.delete_instance()
        return True

    def contains(self, pk):
        message_entry = None
        if self.is_sender:
            message_entry = self.model.get_or_none(self.model.sender_id == pk)
        else:
            message_entry = self.model.get_or_none(self.model.receiver_id == pk)
        if message_entry is None:
            return False
        return True

    def keys(self):
        if self.is_sender:
            return [message.sender_id for message in self.model.select()]
        else:
            return [message.receiver_id for message in self.model.select()]

    def values(self):
        return self.get()

    def get_highest_id(self):
        return self.model.select(fn.Max(MessageModel.message_id)).scalar()


