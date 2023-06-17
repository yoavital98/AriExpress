import json


class Admin:
    def __init__(self, user_name, password, email):
        self.user_name = user_name
        self.password = password
        self.email = email
        self.logged_In = False  # login

        # Getters
    def get_username(self):
        return self.user_name

    def get_password(self):
        return self.password

    def get_email(self):
        return self.email

        # Setters
    def set_username(self, username):
        self.user_name = username

    def set_password(self, password):
        self.password = password

    def get_logged(self):
        return self.logged_In

    def logInAsAdmin(self):
        self.logged_In = True

    def logOffAsAdmin(self):
        self.logged_In = False



    # =======================JSON=======================#

    def toJson(self):
        data = {
            "username": self.user_name,
            "email": self.email
        }
        return json.dumps(data)
