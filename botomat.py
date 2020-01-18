from multiprocessing import Pool
from random import randint

from Task import Task
from RobotEntity import Robot
from data import data
from db import client, db

robot_collection = db["robotlist"]
task_collection = db["tasklist"]

def main():
    while True:
        task_list = convert_task_data()
        print_menu()
        user_input = ""
        while(user_input != "1" and user_input != "2" and user_input != "3"):
            user_input = input("Please enter one of the above menu options: ")
        if(user_input == "1"):
            robot_list = add_robots()
            for i in range(len(robot_list)):
                j = 0
                while j < 5:
                    rand_index = randint(0, len(task_list) - 1)
                    robot_list[i].add_task(task_list[rand_index])
                    j += 1
            indexes = perform_tasks(robot_list)
            update_task_list(indexes)
            sort_leaderboard(robot_list)
        elif(user_input == "2"):
            leaderboard = sort_leaderboard()
            view_leaderboard(leaderboard)
        else:
            break


def update_task_list(indexes):
    task_list = []
    for index in indexes:
        task_list.append(data[index])
    for index in indexes:
        del data[index]
    task_collection.insert_many(task_list)


def perform_tasks(robot_list):
    indexes = set()
    for robot in robot_list:
        task_indexes = robot.do_all_tasks()
        for index in task_indexes:
            if not index in indexes:
                indexes.add(index)
    return indexes


def convert_task_data():
    task_list = []
    for i in range(len(data)):
        description = data[i]["description"]
        eta = data[i]["eta"] / float(1000)
        robot_type = data[i]["robot_type"]
        task = Task(description, eta, robot_type, i)
        task_list.append(task)
    return task_list


def add_robots():
    print("\nPlease enter robot name and type. Separate name and type with a space.")
    print("If you wish to add more than one robot, add a comma to separate the robots with no extra space.")
    print("See following example: Bob Aeronautical,Billy Radial,Joe Bipedal\n")

    user_input = input("Robot(s) List: ")
    robot_list = []
    for entry in user_input.split(","):
        e = entry.split(" ")
        robot = Robot(e[0], e[1])
        robot_list.append(robot)
    dict_list = convert_dict_list(robot_list)
    robot_collection.insert_many(dict_list)
    return robot_list


def convert_dict_list(robot_list):
    dict_list = []
    for robot in robot_list:
        dict_list.append({
            "name": robot.get_robot_name(), 
            "type": robot.get_robot_type(),
            "task_count": robot.get_task_count()
        })
    return dict_list


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