from random import choice
import asyncio
from prettytable import PrettyTable

from Task import Task
from RobotEntity import Robot
from data import data
from db import db

robot_collection = db["robotlist"]
task_collection = db["tasklist"]


def main():
    task_set = create_tasks()
    while True:
        loop = asyncio.get_event_loop()
        print_menu()
        user_input = get_menu_selection()
        if user_input == "1":
            robot_set = create_robots()
            robot_set = assign_tasks(robot_set, task_set)
            perform_tasks(robot_set, loop)
            robot_list = convert_robot_data(robot_set)
            update_leaderboard(robot_list)
        elif user_input == "2":
            view_leaderboard(sort_leaderboard())
        elif user_input == "3":
            view_tasks()
        elif user_input == "4":
            task_set = create_custom_tasks(task_set)
        else:
            loop.close()
            break


def create_custom_tasks(task_set):
    """
    Creates custom tasks based on user's input

    :param task_set: the existing task set that
    :return: task_set: the updated task set with the new task(s) included
    """

    print("\nIn order to create a new custom task, you must enter the relevant details when prompted to. "
          "Please keep in mind that you must enter a valid robot type.\nThese are valid input for robot type: "
          "Unipedal, Bipedal, Quadrupedal, Arachnid, Radial, Aeronautical.\n"
          "NOTE: these tasks may not be picked up by the assignment process and if they are not, new robots "
          "must be created until they are picked up.\n")
    while True:
        description = input("\nPlease enter a description of the task: ")
        eta = float(input("Please enter an estimated time of completion in milliseconds: "))/float(1000)
        robot_type = input("Please enter the type of robot allowed to complete this task: ")
        new_task = Task(description, eta, robot_type)
        task_set.add(new_task)
        user_input = input("\nWould you like to add more tasks (Y/N)?  ")
        if user_input == "N":
            break
    return task_set


def view_tasks():
    """
    View all the completed tasks

    :return:
    """

    all_tasks = task_collection.find()
    # create the output table
    table = PrettyTable(["Description", "ETA(milliseconds)", "Robot Type"])
    table.align["Description"] = "l"
    for record in all_tasks:
        table.add_row([record["description"], record["eta"], record["robot_type"]])
    print(table)


def view_leaderboard(leaderboard):
    """
    View the leaderboard in descending order

    :param leaderboard: the sorted leaderboard from the database
    :return:
    """

    # create the output table
    table = PrettyTable(["Robot Name", "Robot Type", "Task Count", "Completed Tasks"])
    table.align["Completed Tasks"] = "l"
    table.align["Robot Type"] = "l"
    table.align["Robot Name"] = "l"
    for record in leaderboard:
        completed_tasks = set()
        for task in record["completed_tasks"]:
            completed_tasks.add(task["description"])
        table.add_row([record["name"], record["type"], record["task_count"], completed_tasks])
    print(table)


def sort_leaderboard():
    """
    Sorts the robot in descending order by task_count key

    :return: leaderboard: the sorted leaderboard
    """

    leaderboard = robot_collection.find().sort("task_count", -1)
    return leaderboard


def update_leaderboard(robot_list):
    """
    Adds robot(s) to the robot_collection in the database

    :param robot_list: the list of robots that need to be added to the database
    :return:
    """

    robot_collection.insert_many(robot_list)


async def complete_tasks(robot):
    """
    Asynchronous coroutine that waits on robot to do all tasks

    :param robot: the robot doing the tasks
    :return:
    """

    await robot.do_all_tasks()  # wait for the robot to complete all of its tasks
    print(robot.get_robot_name() + " has completed all their tasks.")


def perform_tasks(robot_set, loop):
    """
    Performs all the tasks for all the robots

    :param robot_set: the set of all robots that need to complete tasks
    :param loop: the event loop for the current instance of the application
    :return:
    """

    loop.run_until_complete(asyncio.gather(*(complete_tasks(robot) for robot in robot_set)))


def assign_tasks(robot_set, task_set):
    """
    Randomly assigns tasks to robots from the given task_set

    :param robot_set: the set of robots that need their task sets to be filled
    :param task_set: the set containing tasks that can be randomly assigned to the robots
    :return: robot_set: the set of robots updated with each robots task set
    """

    for robot in robot_set:
        j = 0
        while j < 5:
            random_task = choice(list(task_set))
            while robot.add_task(random_task):
                j += 1
    return robot_set


def create_robots():
    """
    Creates Robot object(s) based off of user input

    :return: robot_set: the newly created set of Robots
    """

    robot_set = set()    
    print("\n- Please enter robot name and type. Separate name and type with a space.")
    print("- If you wish to add more than one robot, add a comma to separate the robots with no extra space.")
    print("  See following example: Bob Aeronautical,Billy Radial,Joe Bipedal")
    
    user_input = input("Robot(s) List: ")
    for entry in user_input.split(","):
        e = entry.split(" ")
        robot = Robot(e[0], e[1])
        robot_set.add(robot)
    return robot_set


def convert_robot_data(robot_set):
    """
    Converts Robot objects to dictionary objects in a list

    :param robot_set: the set of Robot objects
    :return: robot_list: a list of dictionary objects that contain Robot object information
    """

    robot_list = []
    for robot in robot_set:
        robot_list.append({
            "name": robot.get_robot_name(), 
            "type": robot.get_robot_type(),
            "task_count": robot.get_task_count(),
            "completed_tasks": robot.get_completed_task_list()
        })
    return robot_list


def get_menu_selection():
    """
    Gets the user's input for menu selection

    :return: the user's input for menu options
    """

    user_input = ""
    # check for invalid input
    while user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4" and user_input != "5":
        user_input = input("Please enter one of the above menu options: ")
    return user_input


def create_tasks():
    """
    Creates a set of tasks based off of already given task information from data.py

    :return: task_set: a set of Task objects containing all relevant information
    """
    task_set = set()
    for i in range(len(data)):
        description = data[i]["description"]
        eta = data[i]["eta"] / float(1000)
        robot_type = data[i]["robot_type"]
        task = Task(description, eta, robot_type)
        task_set.add(task)
    return task_set


def print_menu():
    """
    Prints the menu options

    :return:
    """
    print("\n1. Add Robot(s)")
    print("2. View Leaderboard")
    print("3. View Completed Tasks")
    print("4. Add Custom Task(s)")
    print("5. Exit")


if __name__ == "__main__":
    main()
