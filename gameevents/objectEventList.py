class ObjectEventList:
    def __init__(self):
        self.events = {}

    def addOrUpdateObjectEvent(self, key, object):
        self.events[key] = object

    def removeEvent(self, key):
        self.events.pop(key, None)

    def getEvent(self, key):
        return self.events.get(key)

    def contains(self, key):
        return key in self.events