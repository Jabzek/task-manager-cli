from dataclasses import dataclass, asdict
from datetime import datetime



@dataclass
class Task:
    name: str
    description: str
    priority: str    #urgent, important, not important
    date_of_creation: str
    deadline: str
    status: str     #active, pending 
    date_of_start: str


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