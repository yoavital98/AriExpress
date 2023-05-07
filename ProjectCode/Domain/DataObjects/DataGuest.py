from ProjectCode.Domain.DataObjects.DataUser import DataUser


class DataGuest(DataUser):
    def __init__(self, guest):
        super().__init__(guest)
