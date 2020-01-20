class Task:
    def __init__(self, description, eta, robot_type):
        self.description = description
        self.eta = eta
        self.robot_type = robot_type

    def __eq__(self, other):
        return self.description == other.description

    def __hash__(self):
        return hash(self.description)

    def get_eta(self):
        return self.eta

    def get_description(self):
        return self.description

    def get_robot_type(self):
        return self.robot_type

    def get_task_info(self):
        return {
            "description": self.get_description(),
            "eta": self.get_eta(),
            "robot_type": self.get_robot_type()
        }