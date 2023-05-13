from ProjectCode.Domain.DataObjects.DataAccess import DataAccess
from ProjectCode.Domain.DataObjects.DataAuction import DataAuction
from ProjectCode.Domain.DataObjects.DataUser import DataUser


class DataMember(DataUser):
    def __init__(self, member):
        super().__init__(member)
        self.accesses = self.getAccesses(member)
        self.email = member.get_email()
        self.auctions = self.getAuctions(member)

    def getAccesses(self, member):
        accesses = dict()
        for key, value in member.accesses.items():
            accesses[key] = DataAccess(value)
        return accesses


    def getAuctions(self, member):
        auctions = dict()
        for key, value in member.auctions.items():
            auctions[key] = DataAuction(value)
        return auctions
