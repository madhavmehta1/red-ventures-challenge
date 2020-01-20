from random import choice
import asyncio

from Task import Task
from RobotEntity import Robot
from data import data
from db import db

robot_collection = db["robotlist"]
task_collection = db["tasklist"]


def main():
    task_set = create_tasks()
    while True:
        print_menu()
        user_input = get_menu_selection()
        if user_input == "1":
            robot_set = create_robots()
            robot_set = assign_tasks(robot_set, task_set)
            perform_tasks(robot_set)
            robot_list = convert_robot_data(robot_set)
            update_leaderboard(robot_list)
        elif user_input == "2":
            view_leaderboard(sort_leaderboard())
        elif user_input == "3":
            view_tasks()
        else:
            break


def view_tasks():
    all_tasks = task_collection.find()
    print("|           Description           |   ETA(seconds)   |   Robot Type   |")
    print("|---------------------------------------------------------------------|")
    output = ""
    for task in all_tasks:
        output = output + "|" + task["description"] + "           |" + str(task["eta"]) + \
                 "           |" + task["robot_type"] + "           |\n"
        output += "|------------------------------------------------------------------------------------------------|\n"
    print(output)


def view_leaderboard(leaderboard):
    print("|   Robot Name   |   Robot Type   |   Task Count   |")
    print("|----------------|----------------|----------------|")
    output = ""
    for record in leaderboard:
        output = output + "|    " + record["name"] + "         |  " + record["type"] + "  |      " \
                 + str(record["task_count"]) + "         |\n"
        output += "|----------------|----------------|----------------|\n"
    print(output)


def sort_leaderboard():
    leaderboard = robot_collection.find().sort("task_count", -1)
    return leaderboard


def update_leaderboard(robot_list):
    robot_collection.insert_many(robot_list)


async def complete_tasks(robot):
    await robot.do_all_tasks()
    print(robot.get_robot_name() + " has completed all their tasks.")


def perform_tasks(robot_set):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*(complete_tasks(robot) for robot in robot_set)))
    loop.close()


def assign_tasks(robot_set, task_set):
    for robot in robot_set:
        j = 0
        while j < 5:
            random_task = choice(list(task_set))
            while robot.add_task(random_task):
                j += 1
    return robot_set


def create_robots():
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
    user_input = ""
    while user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4":
        user_input = input("Please enter one of the above menu options: ")
    return user_input


def create_tasks():
    task_set = set()
    for i in range(len(data)):
        description = data[i]["description"]
        eta = data[i]["eta"] / float(1000)
        robot_type = data[i]["robot_type"]
        task = Task(description, eta, robot_type)
        task_set.add(task)
    return task_set


def print_menu():
    print("1. Add Robot(s)")
    print("2. View Leaderboard")
    print("3. View Completed Tasks")
    print("4. Exit")


if __name__ == "__main__":
    main()
