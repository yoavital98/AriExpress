from ProjectCode.DAL.MemberModel import MemberModel
from ProjectCode.DAL.NominationAgreementModel import NominationAgreementModel
from ProjectCode.Domain.Repository.Repository import Repository


class NominationAgreementRepository(Repository):

    def __init__(self, storename):
        self.model = NominationAgreementModel
        self.storename = storename

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        try:
            return self.add(key, value)
        except Exception as e:
            raise Exception("NominationAgreementRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("NominationAgreementRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
        try:
            return self.contains(item)
        except Exception as e:
            return False

    def get(self, pk=None):
        try:
            if pk is None:
                query = self.model.select().order_by(self.model.username_to_nominate)
                nomination_lists = self.__createNomiationLists(query)
                return nomination_lists
            else:
                accesses_to_nominate_approve_list = []
                nominations_entry = self.model.select().where(self.model.username_to_approve == pk, self.model.store_id == self.storename)
                for nomination in nominations_entry:
                    accesses_to_nominate_approve_list.append(self.__createDomainObject(nomination))
                return accesses_to_nominate_approve_list
        except Exception as e:
            return []

    #returns list of usernames that need to approve the nomination
    def get_by_nominee(self, pk):
        try:
            need_to_approve_list = []
            nominations_entry = self.model.select().where(self.model.username_to_nominate == pk, self.model.store_id == self.storename)
            for nomination in nominations_entry:
                need_to_approve_list.append(nomination.username_to_approve)
            return need_to_approve_list
        except Exception as e:
            return []

    def __createNomiationLists(self, query):
        nomination_list = []
        cur_username = query[0].username_to_nominate
        nomination_list.append(self.__createDomainObject(query[0]))
        for nomination in query:
            if cur_username != nomination.username_to_nominate:
                cur_username = nomination.username_to_nominate
                nomination_list.append(self.__createDomainObject(nomination))
        return nomination_list

    # def __createNomiationLists(self, query):
    #     nomination_lists = []
    #     cur_username = query[0].username_to_approve
    #     cur_list = []
    #     for nomination in query:
    #         if cur_username == nomination.username_to_approve:
    #             cur_list.append(self.__createDomainObject(nomination))
    #         else:
    #             nomination_lists.append(cur_list)
    #             cur_list = []
    #             cur_username = nomination.username_to_approve
    #             cur_list.append(self.__createDomainObject(nomination))
    #     nomination_lists.append(cur_list)
    #     return nomination_lists

    def __createDomainObject(self, nomination_entry):
        from ProjectCode.Domain.MarketObjects.Access import Access
        from ProjectCode.Domain.MarketObjects.Store import Store
        from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member

        user_entry = MemberModel.get(MemberModel.user_name == nomination_entry.username_to_nominate)
        user_dom = Member(user_entry.entrance_id, user_entry.user_name, user_entry.password, user_entry.email)
        store_dom = Store(self.storename)
        access_dom = Access(store_dom, user_dom, nomination_entry.username_requester)
        access_dom.setAccess("Owner")
        return access_dom


    def add(self, username_to_approve, nominated_access):
        nomination_entry = self.model.get_or_none(self.model.username_to_approve == username_to_approve, self.model.username_to_nominate == nominated_access.get_user().get_username(), self.model.store_id == self.storename)
        if nomination_entry is not None:
            #update
            nomination_entry.username_to_approve = username_to_approve
            nomination_entry.username_to_nominate = nominated_access.get_user().get_username()
            nomination_entry.save()
            return True
        self.model.create(username_to_nominate=nominated_access.get_user().get_username(), username_to_approve=username_to_approve, username_requester=nominated_access.get_nominated_by_username(),store_id=self.storename)
        return True


    def remove(self, pk):
        self.model.delete().where(self.model.store_id == self.storename, self.model.username_requester == pk).execute()
        return True

    def remove_nomination(self, nominated_username):
        self.model.delete().where(self.model.store_id == self.storename, self.model.username_to_nominate == nominated_username).execute()
        return True

    #delete single entry
    def remove_by_username_to_approve(self, username_to_approve, username_to_nominate):
        try:
            nomination_entry = self.model.get_or_none(self.model.username_to_approve == username_to_approve, self.model.username_to_nominate == username_to_nominate, self.model.store_id == self.storename)
            if nomination_entry is not None:
                nomination_entry.delete_instance()
                return True
            return False
        except Exception as e:
            raise Exception("NominationAgreementRepository: remove_by_username_to_approve failed: " + str(e))

    def contains(self, pk):
        pass

    def keys(self):
        return [nomination.username_to_approve for nomination in self.model.select()]

    def values(self):
        return self.get()

    # def get_highest_id(self):
    #     return self.model.select(fn.Max(NotificationModel.notification_id)).scalar()

