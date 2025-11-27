import pytest
import json
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from task_manager import action_on_tasks
from task_manager.action_on_tasks import get_date, create_task, Task, delete_task 

@pytest.fixture
def get_date_fixture(monkeypatch):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None) # args - argumenty pozycyjne(*), kwargs(**) - argumenty nazwane
    fake_now = datetime(2025, 5, 14, 12, 30)
    return fake_now


def assert_get_date(final_date, fake_now, shifted_time):
    final_test_date = datetime(shifted_time[0], shifted_time[1], shifted_time[2], 
                               shifted_time[3], shifted_time[4])    
    final_date = datetime.strptime(final_date, "%Y-%m-%d %H:%M")
    assert final_test_date == final_date
    assert final_date > fake_now


@pytest.mark.parametrize("shifted_time", (
    [2026, 4, 13, 7, 20],
    [2025, 12, 1, 1, 0],
    [2025, 5, 15, 10, 0]))


def test_get_date_everything_correct(get_date_fixture, monkeypatch, shifted_time):
    fake_now = get_date_fixture
    shifted_time_copy = shifted_time.copy()
    monkeypatch.setattr("builtins.input", lambda _: shifted_time_copy.pop(0))
    final_date = get_date(fake_now)
    assert_get_date(final_date, fake_now, shifted_time)


@pytest.mark.parametrize("shifted_time, index, value", (
    ([2025, 12, 1, 12, 20], 0, 2024),
    ([2025, 6, 14, 12, 39], 1, 4),
    ([2025, 5, 18, 12, 30], 2, 13)))


def test_get_date_past_date(get_date_fixture, monkeypatch, shifted_time, index, value):
    fake_now = get_date_fixture
    shifted_time_copy = shifted_time.copy()
    shifted_time_copy.insert(index, value)
    monkeypatch.setattr("builtins.input", lambda _: shifted_time_copy.pop(0))
    final_date = get_date(fake_now)
    assert_get_date(final_date, fake_now, shifted_time)


@pytest.mark.parametrize("shifted_time, index, value", ( 
    ([2025, 12, 12, 0, 5], 1, 13),
    ([2030, 4, 30, 1, 35], 2, 31),
    ([2027, 3, 15, 12, 0], 3, 25),
    ([2028, 7, 1, 13, 30], 4, 86)))


def test_get_date_wrong_date(get_date_fixture, monkeypatch, shifted_time, index, value):
    fake_now = get_date_fixture
    shifted_time_copy = shifted_time.copy()
    shifted_time_copy.insert(index, value)
    monkeypatch.setattr("builtins.input", lambda _: shifted_time_copy.pop(0))
    final_date = get_date(fake_now)
    assert_get_date(final_date, fake_now, shifted_time)


@pytest.fixture
def create_task_fixture(monkeypatch, tmp_path):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    task_date_creation = datetime(2025, 5, 14, 12, 30)
    task_date_creation_str = task_date_creation.strftime("%Y-%m-%d %H:%M")
    user_file = tmp_path / "jacek.json"
    user_file.touch()
    return task_date_creation, task_date_creation_str, user_file


@pytest.mark.parametrize("name, description, priority, status, deadline", [
    ("task1", "", "important", "active", datetime(2025, 6, 10, 18, 0).strftime("%Y-%m-%d %H:%M")),
    ("task2", "task2 description", "urgent", "pending", datetime(2025, 9, 11, 18, 0).strftime("%Y-%m-%d %H:%M"))
])


def test_create_task(create_task_fixture, monkeypatch, name, description, priority, status, deadline):
    task_date_creation, task_date_creation_str, user_file = create_task_fixture
    test_task = Task(name, description, priority, status, task_date_creation_str, deadline)
    test_task_dic = test_task.to_dict()
    monkeypatch.setattr(action_on_tasks, "create_task_input", 
                        lambda *_: (name, description, priority, deadline, status))
    create_task(task_date_creation, user_file)

    with open(user_file, "r") as f:
        tasks = json.load(f)

    assert tasks[status][0] == test_task_dic


@pytest.fixture
def delete_task_fixture(monkeypatch, tmp_path):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    user_file = tmp_path / "jacek.json"
    user_file.touch()
    tasks = {
        "pending": [
            {
            "name": "Task2",
            "description": "",
            "priority": "not important",
            "status": "pending",
            "date_of_creation": "2025-11-27 19:13",
            "deadline": "2029-12-12 12:15"
            },
            {
            "name": "Task4",
            "description": "",
            "priority": "important",
            "status": "pending",
            "date_of_creation": "2025-11-27 19:14",
            "deadline": "2026-01-02 03:04"
            }
        ],
        "active": [
            {
            "name": "task1",
            "description": "descripiton for task 1",
            "priority": "important",
            "status": "active",
            "date_of_creation": "2025-11-27 19:12",
            "deadline": "2026-12-12 12:12"
            },
            {
            "name": "Task3",
            "description": "Today is Thursday",
            "priority": "urgent",
            "status": "active",
            "date_of_creation": "2025-11-27 19:13",
            "deadline": "2025-12-31 23:59"
            }
        ],
        "finished": [{
            "name": "Task-1",
            "description": "Today is Wednesday",
            "priority": "urgent",
            "status": "active",
            "date_of_creation": "2025-11-27 19:13",
            "deadline": "2025-11-31 23:59"
            }]
        }

    with open(user_file, "w") as f:
        json.dump(tasks, f)

    return user_file


@pytest.mark.parametrize("task_status, task_index", [
    ("pending", 0),
    ("pending", 1),
    ("active", 0),
    ("active", 1),
    ("finished", 0)
])


def test_delete_task(delete_task_fixture, task_status, task_index):
    user_file = delete_task_fixture
    with open(user_file, "r") as f:
        tasks = json.load(f)
    tasks[task_status].pop(task_index)
    
    delete_task(task_status, task_index, user_file)

    with open(user_file, "r") as f:
        new_tasks = json.load(f)

    assert tasks == new_tasks