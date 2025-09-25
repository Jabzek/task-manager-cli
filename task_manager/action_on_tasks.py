from dataclasses import dataclass, asdict
from datetime import datetime
from dateutil.relativedelta import relativedelta 


@dataclass
class Task:
    name: str
    description: str
    priority: str    #urgent, important, not important
    date_of_creation: str
    deadline: str
    status: str     #active, pending 
    date_of_start: str


def get_date():
    pass