import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

@dataclass
class Task:
    name: str
    description: str
    priority: str    #urgent, important, not important
    date_of_creation: datetime
    deadline: datetime
    status: str     #active, pending, finished 


def get_date(current_time):
    current_year = current_time.year
    current_month = current_time.month
    current_day = current_time.day
    current_hour = current_time.hour
    current_minute = current_time.minute

    while True:
        try:
            year = int(input("Provide year: "))
            if year < current_year:
                raise ValueError
            break
        except ValueError:
            print("Provide correct year. Try again.")

    while True:
        try:
            month = int(input("Provide month: "))
            temp_date = datetime(year, month, day=1)
            if temp_date < datetime(current_year, current_month, day=1):
                raise ValueError
            break
        except ValueError:
            print("Provide correct month. Try again.")

    while True:
        try:
            day = int(input("Provide day: "))
            temp_date = datetime(year, month, day)
            if temp_date < datetime(current_year, current_month, current_day):
                raise ValueError
            break
        except ValueError:
            print("Provide correct day. Try again.")

    while True:
        try:
            hour = int(input("Provide hour: "))
            temp_date = datetime(year, month, day, hour)
            if temp_date < datetime(current_year, current_month, current_day, current_hour):
                raise ValueError
            break
        except ValueError:
            print("Provide correct hour. Try again.")

    while True:
        try:
            minute = int(input("Provide minute: "))
            temp_date = datetime(year, month, day, hour, minute)
            if temp_date <= datetime(current_year, current_month, current_day, current_hour, current_minute):
                raise ValueError
            break
        except ValueError:
            print("Provide correct minute. Try again.")

    return temp_date


def get_task_name(tasks_name):
    while True:
        try:
            name = input("Provide task name: ").strip()
            if not 1 <= len(name) <= 25: 
                raise ValueError
            if name in tasks_name:
                raise NameError
            break
        except ValueError:
            print("The maximum length of a task name is 25.")
        except NameError:
            print("Task name already exists.")
    return name


def get_task_priority():
    while True:
        try:
            priority = input("Provide task priority (urgent, important, not important): ").strip()
            if priority != "urgent" or priority != "important" or priority != "not important":
                raise ValueError
            break
        except ValueError:
            print("Choose urgent, important or not important priority.")
    return priority


def get_status():
    print("Do you want to set the task status to active?")
    while True:
        try:
            active_status = input("Decision: ").strip()
            if active_status == "yes":
                return "active"
            elif active_status == "no":
                return "pending"
            else:
                raise ValueError
        except:
            print("Try again.")


def create_task(creation_date, userfile):
    tasks_name = []
    if Path(userfile).stat().st_size == 0:
        tasks = []
    else:
        with open(userfile, "r") as f:
            tasks = json.load(f)
    for el in tasks:
        tasks_name.append(el["name"])

    name = get_task_name(tasks_name)
    descripiton = input("Provide description of the task: ")
    priority = get_task_priority()
    deadline = get_date(creation_date)
    status = get_status()

    task = Task(name, descripiton, priority, creation_date, deadline, status)