class Response:
    def __init__(self, returnValue, status):
        self.return_value = returnValue
        self.status = status

    def getStatus(self):
        return self.status

    def getReturnValue(self):
        return self.return_value
