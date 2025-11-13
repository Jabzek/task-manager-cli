import pytest
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from task_manager import action_on_profiles
from task_manager.action_on_profiles import saving_new_profile, log_into_profile, del_profile, saving_new_password

@pytest.fixture
def mock_environment(monkeypatch, tmp_path):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    monkeypatch.setattr(action_on_profiles, "get_file", lambda name: tmp_path / f"{name}.json")
    users_file = tmp_path / "users.json"
    return users_file


@pytest.mark.parametrize("username, password", [
    ("jacek", "123"),
    ("Kobi!!!", "shdgfhbsf")
])


def test_save_new_profile(mock_environment, tmp_path, username, password):
    users_file = mock_environment
    user_file = tmp_path / (username + ".json")
    user_data = {"username": username,
                 "password": password,
                 "file": str(user_file)}
    test_user_data = saving_new_profile(users_file, user_file, username, password)

    assert user_data == test_user_data
    assert user_file.exists()

    with open(users_file, "r") as f:
        data = json.load(f)    

    assert user_data in data


def saving_data_to_file(users_file, tmp_path):
    file_list = (str(tmp_path / "jacek.json"), str(tmp_path / "leon4jds.json"), str(tmp_path / "ann531.json"),
                str(tmp_path / "johnus941.json"))
    data = [{"username": "jacek", "password": "123", "file": file_list[0]},
            {"username": "leon4jds", "password": "F@BafvLOP", "file": file_list[1]},
            {"username": "ann531", "password": "hobbit123", "file": file_list[2]},
            {"username": "johnus941", "password": "arZWksPP", "file": file_list[3]}]
    with open(users_file, "w") as f:
        json.dump(data, f)

    for file in file_list:
        Path(file).touch()


def assert_profiles_login(username, password, result, tmp_path):
    user_data = {"username": username, "password": password, "file": str(tmp_path / f"{username}.json")}
    assert result == user_data

@pytest.mark.parametrize("username, password", [
    ("jacek", "123"),
    ("ann531", "hobbit123"),
    ("leon4jds", "F@BafvLOP")])


def test_log_into_profile_everything_correct(mock_environment, monkeypatch, username, password, tmp_path):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    inputs = [username, password]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    result = log_into_profile(users_file)
    assert_profiles_login(username, password, result, tmp_path)
    

@pytest.mark.parametrize("username1, username2, password", [
    ("jabzek", "jacek", "123"),
    ("max3kjn", "leon4jds", "F@BafvLOP"),
    ("JOHNUS941", "johnus941", "arZWksPP")])


def test_log_into_profile_user_does_not_exist(mock_environment, monkeypatch, username1, username2, password, tmp_path):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    inputs = [username1, username2, password]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    result = log_into_profile(users_file)
    assert_profiles_login(username2, password, result, tmp_path)


@pytest.mark.parametrize("username, password1, password2", [
    ("jacek", "321", "123"),
    ("leon4jds", "ASFnvdj312Agdf@", "F@BafvLOP"),
    ("ann531", "vader123", "hobbit123")])


def test_log_into_profile_wrong_password(mock_environment, monkeypatch, username, password1, password2, tmp_path):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    inputs = [username, password1, username, password2]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    result = log_into_profile(users_file)
    assert_profiles_login(username, password2, result, tmp_path)


@pytest.mark.parametrize("user_data", [
    {"username": "jacek", "password": "123"},
    {"username": "leon4jds", "password": "F@BafvLOP"}
])


def test_delete_profile(mock_environment, tmp_path, user_data):
    users_file = mock_environment
    file = tmp_path / (user_data["username"] + ".json")
    user_data["file"] = str(file)
    saving_data_to_file(users_file, tmp_path)
    del_profile(users_file, user_data)

    assert not file.exists()

    with open(users_file, "r") as f:
        data = json.load(f)

    assert user_data not in data


@pytest.mark.parametrize("username, new_password", [
    ("jacek", "321"),
    ("ann531", "GRAc1n")
])


def test_change_password(mock_environment, tmp_path, username, new_password):
    users_file = mock_environment
    new_user_data = {"username": username, "password": new_password, "file": str(tmp_path / (username + ".json"))}
    saving_data_to_file(users_file, tmp_path)
    test_user_data = saving_new_password(users_file, username, new_password)

    assert test_user_data == new_user_data

    with open(users_file, "r") as f:
        data = json.load(f)

    for el in data:
        if username == el["username"]:
            assert new_password == el["password"]
