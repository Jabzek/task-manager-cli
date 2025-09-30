import pytest
import json
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from task_manager.action_on_tasks import get_date, create_task

@pytest.fixture
def get_date_fixture(monkeypatch):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    fake_now = datetime(2025, 5, 14, 12, 30)
    return fake_now


def assert_get_date(final_date, fake_now, shifted_time):
    final_test_date = datetime(shifted_time[0], shifted_time[1], shifted_time[2], 
                               shifted_time[3], shifted_time[4])    
        
    assert final_test_date == final_date
    assert final_date > fake_now


@pytest.mark.parametrize("shifted_time", (
    [2026, 4, 13, 7, 20],
    [2025, 12, 1, 1, 0],
    [2025, 5, 15, 10, 0]))


def test_get_date_everything_correct(create_task_fixture, monkeypatch, shifted_time):
    fake_now = create_task_fixture
    shifted_time_copy = shifted_time.copy()
    monkeypatch.setattr("builtins.input", lambda _: shifted_time_copy.pop(0))
    final_date = get_date(fake_now)
    assert_get_date(final_date, fake_now, shifted_time)


@pytest.mark.parametrize("shifted_time, index, value", (
    ([2025, 12, 1, 12, 20], 0, 2024),
    ([2025, 6, 14, 12, 39], 1, 4),
    ([2025, 5, 18, 12, 30], 2, 13)))


def test_get_date_past_date(create_task_fixture, monkeypatch, shifted_time, index, value):
    fake_now = create_task_fixture
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


def test_get_date_wrong_date(create_task_fixture, monkeypatch, shifted_time, index, value):
    fake_now = create_task_fixture
    shifted_time_copy = shifted_time.copy()
    shifted_time_copy.insert(index, value)
    monkeypatch.setattr("builtins.input", lambda _: shifted_time_copy.pop(0))
    final_date = get_date(fake_now)
    assert_get_date(final_date, fake_now, shifted_time)


@pytest.fixture
def create_task_fixture(monkeypatch, tmp_path):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    task_date_creation = datetime(2025, 5, 14, 12, 30)
    user_file = tmp_path / "jacek.json"
    return task_date_creation, user_file


def saving_date(user_file, task_date_creation):
    data = [{"name": "task1", "description": "description1", "priority": "urgent",
            "date_of_creation": task_date_creation, "deadline": datetime(2025, 6, 10, 18, 0),
            "status": "pending"},
            {"name": "name_taken", "description": "description2", "priority": "important",
            "date_of_creation": task_date_creation, "deadline": datetime(2025, 9, 11, 18, 0),
            "status": "pending"},
            {"name": "task2", "description": "description3", "priority": "urgent",
            "date_of_creation": task_date_creation, "not important": datetime(2026, 2, 1, 15, 0),
            "status": "pending"}]
    with open(user_file, "w") as f:
        json.dump(data, f, indent=2)


def assert_task_create(user_file, task):
    with open(user_file, "r") as f:
        tasks = json.load(f)
    assert task in tasks


@pytest.mark.parametrize("name, description, priority, deadline", (
    ("task1", "description1", "urgent", "2025-6-10-18-00"),
    ("task2", "descripiton2", "important", "2025-9-11-15-00"),
    ("task3", "", "not important", "2026-3-17-19-00")))


def test_create_task_adding_first_task(monkeypatch, create_task_fixture, name, description, priority, deadline):
    task_date_creation, user_file = create_task_fixture
    deadline = datetime.strptime(deadline, "%Y-%m-%d-%H-%M")
    inputs = [name, description, priority, deadline]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    task = {"name": name, "description": description, "priority": priority,
            "date_of_creation": task_date_creation, "deadline": deadline,
            "status": "pending"}
    create_task(task_date_creation, user_file)
    assert_task_create(user_file, task)


@pytest.mark.parametrize("wrong_name, name, description, wrong_priority, priority, deadline", (
    ("a" * 30, "task1", "description1", "good", "urgent", "2025-6-10-18-00"),
    ("", "1", "descripiton2", "bad", "important", "2025-9-11-15-00"),
    ("name_taken", "1", "descripiton3", "insteresting", "important", "2025-9-11-15-00")))


def test_create_task_wrong_name_and_priority(monkeypatch, create_task_fixture, wrong_name, name, description, wrong_priority, priority, deadline):
    task_date_creation, user_file = create_task_fixture
    deadline = datetime.strptime(deadline, "%Y-%m-%d-%H-%M")
    inputs = [wrong_name, name, description, wrong_priority, priority, deadline]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    task = {"name": name, "description": description, "priority": priority,
            "date_of_creation": task_date_creation, "deadline": deadline,
            "status": "pending"}
    saving_date(user_file, task_date_creation)
    create_task(task_date_creation, user_file)
    assert_task_create(user_file, task)


@pytest.mark.parametrize("name, description, priority, deadline", (
    ("task4", "description1", "urgent", "2025-5-20-18-00"),
    ("task5", "descripiton2", "important", "2025-9-11-15-00"),
    ("task6", "", "not important", "2026-3-17-19-00")))


def test_create_task_adding_another_task(monkeypatch, create_task_fixture, name, description, priority, deadline):
    task_date_creation, user_file = create_task_fixture
    deadline = datetime.strptime(deadline, "%Y-%m-%d-%H-%M")
    inputs = [name, description, priority, deadline]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    task = {"name": name, "description": description, "priority": priority,
            "date_of_creation": task_date_creation, "deadline": deadline,
            "status": "pending"}
    saving_date(user_file, task_date_creation)
    create_task(task_date_creation, user_file)
    assert_task_create(user_file, task)