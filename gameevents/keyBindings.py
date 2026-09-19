class KeyBindingRegistry:
    def __init__(self):
        self.bindings = {}

    def register(self, objectName, bindings):
        self.bindings[objectName] = bindings

    def getBindings(self, objectName):
        return self.bindings.get(objectName, {})

    def objectNames(self):
        return self.bindings.keys()
