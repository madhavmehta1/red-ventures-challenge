import time
from multiprocessing import Pool
import asyncio
import itertools


class Robot:
    def __init__(self, robot_name, robot_type):
        self.robot_name = robot_name
        self.robot_type = robot_type
        self.task_count = 0
        self.task_set = set()


    @asyncio.coroutine
    async def do_task(self, task):
        await asyncio.sleep(task.get_eta())
        print(self.get_robot_name() + " has finished task: " + task.get_description())
        if task.get_robot_type() == self.get_robot_type():
            self.task_count += 1
        return task.get_description()
    

    async def do_all_tasks(self, task_set):
        loop = asyncio.get_event_loop()
        args = [task for task in task_set]
        tasks = itertools.starmap(do_task, args)
        completed_tasks = loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()
        return completed_tasks


    def get_robot_name(self):
        return self.robot_name
    

    def get_robot_type(self):
        return self.robot_type


    def get_task_count(self):
        return self.task_count
    

    def get_task_set(self):
        return self.task_set


    def add_task(self, task):
        if task in self.task_set:
            return False
        else:
            self.task_set.add(task)
            return True