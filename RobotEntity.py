import asyncio

from db import db
task_collection = db["tasklist"]


class Robot:
    """
    A robot that asynchronously completes tasks that it is assigned.
    """
    def __init__(self, robot_name, robot_type):
        """
        Initialize the Robot

        :param robot_name: represents the robot's name
        :param robot_type: represents the robot's type
        """
        self.robot_name = robot_name
        self.robot_type = robot_type
        self.task_count = 0
        self.task_set = set()
        self.completed_task_list = []

    async def do_task(self, task):
        """
        Asynchronous coroutine that 'does' the provided task.

        :param task: the task that needs to be completed
        :return: result: the number of times the task occurs in the the task_collection
        """

        await asyncio.sleep(task.get_eta())  # the program waits for the amount of time specified by the task's eta
        print(self.get_robot_name() + " has finished task: " + task.get_description())
        if task.get_robot_type() == self.get_robot_type():
            # if the robot types match for the robot and the task, then give the robot credit
            self.increment_task_count()
        self.task_set.remove(task)  # remove the task from the robot's task set
        completed_task = {
            "description": task.get_description(),
            "eta": task.get_eta()*1000,
            "robot_type": task.get_robot_type()
        }
        # add this newly completed task to the robot's completed task list
        self.completed_task_list.append(completed_task)
        result = task_collection.count_documents({"description": task.get_description()})
        if result == 0:
            # if the task is not already in the task_collection, add it
            task_collection.insert_one(completed_task)
        return result

    async def do_all_tasks(self):
        """
        Asynchronous coroutine that 'does' all the tasks assigned to the robot

        :return:
        """

        # allows for the robot to 'do' all the tasks in the task set asynchronously
        await asyncio.gather(*(self.do_task(task) for task in self.task_set))
        print(self.get_robot_name() + " has finished all their tasks." + " Their task queue has " +
              str(len(self.task_set)) + " items." + " Their task count is now " + str(self.get_task_count()))

    def increment_task_count(self):
        """
        Increments the robots task count

        :return:
        """

        self.task_count += 1

    def get_robot_name(self):
        """
        Gets the robot's name

        :return: the robot's name
        """

        return self.robot_name

    def get_robot_type(self):
        """
        Gets the robot's type

        :return: the robot's type
        """

        return self.robot_type

    def get_task_count(self):
        """
        Get's the robot's task count

        :return: the robot's task count
        """

        return self.task_count

    def get_task_set(self):
        """
        Get's the robot's task set

        :return: the robot's task set
        """

        return self.task_set

    def get_completed_task_list(self):
        """
        Get's the robot's completed task list

        :return: the robot's completed task list
        """

        return self.completed_task_list

    def add_task(self, task):
        """
        Add the given task to the robot's task set only if it isn't already

        :param task: the task that needs to be added to the robot's task set
        :return: a boolean True or False indicating whether the task can be added to the robot's task set
        """

        if task in self.task_set:
            # if the task is already in the robot's task set, return False indicating that it cannot be added
            return False
        else:
            self.task_set.add(task)
            return True
