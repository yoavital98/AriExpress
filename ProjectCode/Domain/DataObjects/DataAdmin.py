class DataAdmin:
    def __init__(self, admin):
        self.user_name = admin.get_username()
        self.email = admin.get_email()
        self.logged_In = admin.get_logged() # login