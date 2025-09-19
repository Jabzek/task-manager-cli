import pytest
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from task_manager import action_on_profiles
from task_manager.action_on_profiles import create_profile

@pytest.fixture
def mock_environment(monkeypatch, tmp_path):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    monkeypatch.setattr(action_on_profiles, "get_file", lambda name: tmp_path / f"{name}.json")
    users_file = tmp_path / "users.json"
    return users_file


@pytest.mark.parametrize("username, password", [
    ("jacek", "123"),
    ("zxddfajshflkmfasdf", "fdsjkh13AFDJAKF!#!#!"),
    ("Magda123", "d3D!gdfnXPor")])


def test_create_profile_everything_correct(mock_environment, monkeypatch, username, password):
    users_file = mock_environment
    inputs = [username, password, password]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    result = create_profile(users_file)

    assert result["username"] == username
    assert result["password"] == password
    assert Path(result["file"]).exists()

    with open(users_file, "r") as f:
        data = json.load(f)
    assert data == [result]