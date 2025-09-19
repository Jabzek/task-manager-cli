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


def assert_profiles(result, username, password, users_file):
    assert result["username"] == username
    assert result["password"] == password
    assert Path(result["file"]).exists()

    with open(users_file, "r") as f:
        data = json.load(f)
    assert result in data


@pytest.mark.parametrize("username, password", [
    ("jacek", "123"),
    ("zxddfajshflkmfasdf", "fdsjkh13AFDJAKF!#!#!"),
    ("Magda123", "d3D!gdfnXPor")])


def test_create_profile_everything_correct(mock_environment, monkeypatch, username, password):
    users_file = mock_environment
    inputs = [username, password, password]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    result = create_profile(users_file)
    assert_profiles(result, username, password, users_file)


@pytest.mark.parametrize("username1, password, username2", [
    ("jacek", "123", "jabzek"),
    ("John321", "!DSgdfkmap", "John12345!")])


def test_create_profile_user_exists(mock_environment, monkeypatch, username1, password, username2, tmp_path):
    users_file = mock_environment
    inputs = [username1, username2, password, password]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    Path.touch(tmp_path / f"{username1}.json")
    result = create_profile(users_file)
    assert_profiles(result, username2, password, users_file)


@pytest.mark.parametrize("username, password1, password2, password", [
    ("jacek", "123", "321", "123"),
    ("William654$", "gkap3vmASB", "Gkap3vmASB", "h2VA!#FDDDA")])


def test_create_profile_different_passwords(mock_environment, monkeypatch, username, password1, password2, password):
    users_file = mock_environment
    inputs = [username, password1, password2, password, password]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    result = create_profile(users_file)
    assert_profiles(result, username, password, users_file)


@pytest.mark.parametrize("username, password", [
    ("jacek", "123"),
    ("zxddfajshflkmfasdf", "fdsjkh13AFDJAKF!#!#!"),
    ("Magda123", "d3D!gdfnXPor")])


def test_create_profile_second_user(mock_environment, monkeypatch, username, password, tmp_path):
    users_file = mock_environment
    inputs = [username, password, password]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    users_data = {"username": "Tomato5214",
                  "password": "Potato9185",
                  "file": f"{tmp_path} / Tomato5214.json"}
    
    with open(users_file, "w") as f:
        json.dump([users_data], f)
    result = create_profile(users_file)
    
    with open(users_file, "r") as f:
        data = json.load(f)
    
    assert len(data) == 2
    assert data[0] == users_data
    assert data[1] == result