from peewee import fn

from ProjectCode.DAL.NotificationModel import NotificationModel
from ProjectCode.Domain.ExternalServices.MessageObjects.Notfication import Notification
from ProjectCode.Domain.Repository.Repository import Repository


class NotificationRepository(Repository):

    def __init__(self):
        self.model = NotificationModel

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("NotificationRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("NotificationRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
        try:
            return self.contains(item)
        except Exception as e:
            return False

    def get(self, pk=None):
        try:
            if pk is None:
                query = NotificationModel.select().order_by(NotificationModel.receiver_id)
                notification_lists = self.__createNotificationLists(query)
                return notification_lists
            else:
                notification_list = []
                notification_entry = NotificationModel.select().where(NotificationModel.receiver_id == pk)
                for notification in notification_entry:
                    notification_list.append(self.__createDomainObject(notification))
                return notification_list
        except Exception as e:
            return []

    def __createNotificationLists(self, query):
        notification_lists = []
        cur_username = query[0].receiver_id
        cur_list = []
        for notification in query:
            if cur_username == notification.receiver_id:
                cur_list.append(self.__createDomainObject(notification))
            else:
                notification_lists.append(cur_list)
                cur_list = []
                cur_username = notification.receiver_id
                cur_list.append(self.__createDomainObject(notification))
        notification_lists.append(cur_list)
        return notification_lists

    def __createDomainObject(self, notification_entry):
        notification_dom = Notification(notification_entry.notification_id, notification_entry.sender_id, notification_entry.receiver_id, notification_entry.subject, notification_entry.content, notification_entry.date)
        if notification_entry.read:
            notification_dom.mark_as_read()
        return notification_dom

    def add(self, notification):
        notification_entry = self.model.get_or_none(self.model.notification_id == notification.get_id())
        if notification_entry is not None:
            #update
            notification_entry.sender_id = notification.get_sender_id()
            notification_entry.receiver_id = notification.get_receiver_id()
            notification_entry.subject = notification.get_subject()
            notification_entry.content = notification.get_content()
            notification_entry.date = notification.get_date()
            notification_entry.read = notification.is_read()
            notification_entry.save()
            return notification
        NotificationModel.create(sender_id=notification.get_sender_id(), receiver_id=notification.get_receiver_id(), subject=notification.get_subject(), content=notification.get_content(), date=notification.get_date())
        return notification

    def remove(self, pk):
        notification_entry = self.model.get(self.model.notification_id == pk)
        notification_entry.delete_instance()
        return True

    def contains(self, pk):
        notification_entry = self.model.get_or_none(self.model.receiver_id == pk)
        if notification_entry is None:
            return False
        return True

    def keys(self):
        return [notification.receiver_id for notification in self.model.select()]

    def values(self):
        return self.get()

    def get_highest_id(self):
        return self.model.select(fn.Max(NotificationModel.notification_id)).scalar()


