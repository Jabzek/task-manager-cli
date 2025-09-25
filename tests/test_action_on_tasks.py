import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from task_manager.action_on_tasks import get_date 


@pytest.fixture
def mock_environment_get_date(monkeypatch):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    fake_now = datetime.now()
    monkeypatch.setattr(datetime, "now", lambda: fake_now)
    return fake_now


def time_shift(shifts, fake_now):
    shifted_time = [fake_now.year + relativedelta(years=shifts[0]),
                    fake_now.month + relativedelta(months=shifts[1]),
                    fake_now.day + relativedelta(days=shifts[2]),
                    fake_now.hour + relativedelta(hours=shifts[3]),
                    fake_now.minute + relativedelta(minutes=shifts[4])]
    return shifted_time


def assert_get_date(final_date, fake_now, shifted_time):
    final_test_date = datetime(shifted_time[0], shifted_time[1], shifted_time[2], 
                               shifted_time[3], shifted_time[4])    
        
    assert final_test_date == final_date
    assert final_date > fake_now


@pytest.mark.parametrize("shifts", ( 
    [1, 2, 12, 3, 5],
    [12, 5, 10, 11, 3],
    [35, 0, 0, 12, 0]))


def test_get_date_everything_correct(mock_environment_get_date, monkeypatch, shifts):
    fake_now = mock_environment_get_date
    shifted_time = time_shift(shifts, fake_now)
    monkeypatch.setattr("builtins.input", lambda _: shifted_time.pop(0))
    final_date = get_date()
    assert_get_date(final_date, fake_now, shifted_time)


@pytest.mark.parametrize("shifts", (
    [-1, 2, 12, 3, 5, 1, 2, 12, 3, 5],
    [0, -1, 0, 12, 0, 0, 1, 0, 12, 0],
    [0, 0, -5, 23, 24, 0, 0, 5, 23, 24]))


def test_get_date_wrong_date(mock_environment_get_date, monkeypatch, shifts):
    fake_now = mock_environment_get_date
    shifted_time_wrong = time_shift(shifts[:5], fake_now)
    shifted_time_correct = time_shift(shifts[5:], fake_now)
    shifted_time = []

    for idx in range(5):
        if shifted_time_wrong[idx] == shifted_time_correct[idx]:
            shifted_time.append(shifted_time_correct[idx])
        else:
            shifted_time.append(shifted_time_wrong[idx])
            shifted_time.append(shifted_time_correct[idx])

    monkeypatch.setattr("builtins.input", lambda _: shifted_time.pop(0))
    final_date = get_date()
    assert_get_date(final_date, fake_now, shifted_time_correct)