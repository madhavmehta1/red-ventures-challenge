class Task:
    def __init__(self, description, eta, robot_type, task_index):
        self.description = description
        self.eta = eta
        self.robot_type = robot_type
        self.task_index = task_index
    
    def get_eta(self):
        return self.eta
    
    def get_description(self):
        return self.description

    def get_robot_type(self):
        return self.robot_type

    def get_task_index(self):
        return self.task_index