class RegistrationModule:
    def __init__(self):
        self.members = {}
    def register(self, name):
        if name in self.members: return False
        self.members[name] = "Unassigned"
        return True
    def is_registered(self, name):
        return name in self.members
