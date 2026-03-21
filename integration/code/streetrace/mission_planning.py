class MissionPlanningModule:
    def __init__(self, crew_mod, inv_mod):
        self.crew = crew_mod
        self.inv = inv_mod
    def start_mission(self, role_req, reward):
        if any(role == role_req for role in self.crew.reg.members.values()):
            self.inv.add_cash(reward)
            if role_req == "mechanic":
                for c in self.inv.get_cars():
                    c["condition"] = 100
            return True
        raise ValueError(f"Required role {role_req} not available.")
