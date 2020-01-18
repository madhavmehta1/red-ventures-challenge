import time
from multiprocessing import Pool

# from db import client, db

# robot_collection = db["robotlist"]

class Robot:
    def __init__(self, robot_name, robot_type):
        self.robot_name = robot_name
        self.robot_type = robot_type
        self.task_count = 0
        self.task_list = []

    def do_task(self, task):
        time.sleep(task.get_eta())
        print(self.get_robot_name() + "has finished task: " + task.get_description())
        if task.get_robot_type() == self.get_robot_type:
                increment_task_count()
        return task.get_task_index()

    def do_all_tasks(self):
        with Pool(2) as p:
            return p.map(self.do_task, self.get_task_list())

    def get_robot_name(self):
        return self.robot_name
    
    def get_robot_type(self):
        return self.robot_type

    def get_task_count(self):
        return self.task_count
    
    def get_task_list(self):
        return self.task_list
    
    def increment_task_count(self):
        self.task_count += 1

    def add_task(self, task):
        self.task_list.append(task)


    # def set_object_id(self):
    #     query = {
    #         "name" : self.get_robot_name,
    #         "type" : self.get_robot_type
    #     }
    #     result = robot_collection.find(query, {"_id": 1, "name": 0, "task_count": 0})
    #     self.object_id = result


    # def get_object_id(self):
    #     return self.object_id        
