import asyncio

from db import db
task_collection = db["tasklist"]


class Robot:
    def __init__(self, robot_name, robot_type):
        self.robot_name = robot_name
        self.robot_type = robot_type
        self.task_count = 0
        self.task_set = set()
        self.completed_task_list = []

    async def do_task(self, task):
        await asyncio.sleep(task.get_eta())
        print(self.get_robot_name() + " has finished task: " + task.get_description())
        if task.get_robot_type() == self.get_robot_type():
            self.increment_task_count()
        self.task_set.remove(task)
        completed_task = {
            "description": task.get_description(),
            "eta": task.get_eta(),
            "robot_type": task.get_robot_type()
        }
        self.completed_task_list.append(completed_task)
        if task_collection.find({"description": task.get_description(), "eta": task.get_eta(),
                                "robot_type": task.get_robot_type()}):
            pass
        else:
            task_collection.insert_one(completed_task)

    async def do_all_tasks(self):
        await asyncio.gather(*(self.do_task(task) for task in self.task_set))
        print(self.get_robot_name() + " has finished all their tasks." + " Their task queue has " +
              str(len(self.task_set)) + " items." + " Their task count is now " + str(self.get_task_count()))

    def increment_task_count(self):
        self.task_count += 1

    def get_robot_name(self):
        return self.robot_name

    def get_robot_type(self):
        return self.robot_type

    def get_task_count(self):
        return self.task_count

    def get_task_set(self):
        return self.task_set

    def get_completed_task_list(self):
        return self.completed_task_list

    def add_task(self, task):
        if task in self.task_set:
            return False
        else:
            self.task_set.add(task)
            return True
