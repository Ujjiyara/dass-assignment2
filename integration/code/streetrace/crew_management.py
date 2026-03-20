class CrewManagementModule:
    def __init__(self, registration_module):
        self.reg = registration_module
        self.skills = {}
    def assign_role(self, name, role, skill):
        if not self.reg.is_registered(name):
            raise ValueError("Must register first.")
        self.reg.members[name] = role
        self.skills[name] = skill
    def get_role(self, name):
        return self.reg.members.get(name)
