import pytest
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from task_manager.action_on_tasks import get_date 


def assert_get_date(final_date, fake_now, shifted_time):
    final_test_date = datetime(shifted_time[0], shifted_time[1], shifted_time[2], 
                               shifted_time[3], shifted_time[4])    
        
    assert final_test_date == final_date
    assert final_date > fake_now


@pytest.mark.parametrize("shifted_time", (
    [2026, 4, 13, 7, 20],
    [2025, 12, 1, 1, 0],
    [2025, 5, 15, 10, 0]))


def test_get_date_everything_correct(monkeypatch, shifted_time):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    fake_now = datetime(2025, 5, 14, 12, 30)
    shifted_time_copy = shifted_time.copy()
    monkeypatch.setattr("builtins.input", lambda _: shifted_time_copy.pop(0))
    final_date = get_date(fake_now)
    assert_get_date(final_date, fake_now, shifted_time)


@pytest.mark.parametrize("shifted_time, index, value", (
    ([2025, 12, 1, 12, 20], 0, 2024),
    ([2025, 6, 14, 12, 39], 1, 4),
    ([2025, 5, 18, 12, 30], 2, 13)))


def test_get_date_past_date(monkeypatch, shifted_time, index, value):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    fake_now = datetime(2025, 5, 14, 12, 30)
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


def test_get_date_wrong_date(monkeypatch, shifted_time, index, value):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    fake_now = datetime(2025, 5, 14, 12, 30)
    shifted_time_copy = shifted_time.copy()
    shifted_time_copy.insert(index, value)
    monkeypatch.setattr("builtins.input", lambda _: shifted_time_copy.pop(0))
    final_date = get_date(fake_now)
    assert_get_date(final_date, fake_now, shifted_time)