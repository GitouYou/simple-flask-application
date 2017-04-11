class Currency(object):

    def __init__(self, initial):
        self._initial = initial
        self.obj = {
            "startDate": "",
            "data": [],
            "name": self._initial
        }

    def initials(self):
        return self._initial

    def set(self, startDate, data):
        self.obj["data"] = data
        self.obj["startDate"] = startDate


    def __str__(self):
        if self.obj:
            return self._initial
        return ''
