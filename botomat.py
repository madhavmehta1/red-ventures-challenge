from multiprocessing import Pool
from random import choice
import asyncio
import itertools

from Task import Task
from RobotEntity import Robot
from data import data
from db import client, db

robot_collection = db["robotlist"]
task_collection = db["tasklist"]

def main():
    # while True:
    #     task_list = convert_task_data()
    #     print_menu()
    #     user_input = ""
    #     while(user_input != "1" and user_input != "2" and user_input != "3"):
    #         user_input = input("Please enter one of the above menu options: ")
    #     if(user_input == "1"):
    #         robot_list = add_robots()
    #         for i in range(len(robot_list)):
    #             j = 0
    #             while j < 5:
    #                 rand_index = randint(0, len(task_list) - 1)
    #                 robot_list[i].add_task(task_list[rand_index])
    #                 j += 1
    #         indexes = perform_tasks(robot_list)
    #         update_task_list(indexes)
    #         sort_leaderboard(robot_list)
    #     elif(user_input == "2"):
    #         leaderboard = sort_leaderboard()
    #         view_leaderboard(leaderboard)
    #     else:
    #         break
    task_set = create_tasks()
    while True:
        print_menu()
        user_input = select_menu_selection()
        if user_input == "1":
            robot_set = create_robots()
            assign_tasks(robot_set)
            perform_tasks(robot_set)
        elif user_input == "2":
            view_leaderboard()
        elif user_input == "3":
            view_tasks()
        else:
            break





@asyncio.coroutine
async def complete_tasks(robot):
    await robot.do_all_tasks()
    print(robot.get_robot_name() +  " has completed all their tasks.")

def perform_tasks(robot_set):
    loop = asyncio.get_event_loop()
    args = [robot for robot in robot_set]
    tasks = itertools.starmap(complete_tasks, args)
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()


def assign_tasks(robot_set):
    for robot in robot_set:
        j = 0
        while j < 5:
            random_task = choice(list(robot_set))
            while robot.add_task(random_task):
                j += 1


def create_robots():
    robot_set = set()    
    print("\n- Please enter robot name and type. Separate name and type with a space.")
    print("- If you wish to add more than one robot, add a comma to separate the robots with no extra space.")
    print("  See following example: Bob Aeronautical,Billy Radial,Joe Bipedal")
    
    user_input = input("Robot(s) List: ")
    invalid_names = []
    for entry in user_input.split(","):
        e = entry.split(" ")           
        robot = Robot(e[0, e[1]])
       robot_set.add(robot)
    # dict_list = convert_dict_list(robot_set)
    # robot_collection.insert_many(dict_list)
    return robot_set


def convert_robot_data(robot_set):
    robot_list = []
    for robot in robot_set:
        robot_list.append({
            "name": robot.get_robot_name(), 
            "type": robot.get_robot_type(),
            "task_count": robot.get_task_count(),
            "completed_tasks": robot.get_task_set()
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
        task = Task(description, eta, robot_type, i)
        task_set.add(task)
    return task_set


# def update_task_list(indexes):
#     task_list = []
#     for index in indexes:
#         task_list.append(data[index])
#     for index in indexes:
#         del data[index]
#     task_collection.insert_many(task_list)


# def perform_tasks(robot_list):
#     indexes = set()
#     for robot in robot_list:
#         task_indexes = robot.do_all_tasks()
#         for index in task_indexes:
#             if not index in indexes:
#                 indexes.add(index)
#     return indexes


# def find_robot(name):
#     if robot_collection.find_one({"name": name}) == None:
#         return True
#     return False


def print_menu():
    print("1. Add Robot(s)")
    print("2. View Leaderboard")
    print("3. Exit")


def view_leaderboard(leaderboard):
    print("|   Robot Name   |   Robot Type   |   Task Count   |")
    print("|----------------|----------------|----------------|")
    output = ""
    for record in leaderboard:
        output = output + "|    " + record["name"] + "         |  " + record["type"] + "  |      " + str(record["task_count"]) + "         |\n"
        output += "|----------------|----------------|----------------|\n"
    print(output)


def sort_leaderboard():
    leaderboard = robot_collection.find().sort("task_count", -1)
    return leaderboard

if __name__ == "__main__":
    main()