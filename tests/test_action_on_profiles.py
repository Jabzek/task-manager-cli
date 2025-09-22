import pytest
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from task_manager import action_on_profiles
from task_manager.action_on_profiles import create_profile, log_into_profile, delete_profile, change_password

@pytest.fixture
def mock_environment(monkeypatch, tmp_path):
    monkeypatch.setattr("builtins.print", lambda *a, **kw: None)
    monkeypatch.setattr(action_on_profiles, "get_file", lambda name: tmp_path / f"{name}.json")
    users_file = tmp_path / "users.json"
    return users_file


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


def assert_profiles_creation(result, username, password, users_file):
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
    assert_profiles_creation(result, username, password, users_file)


@pytest.mark.parametrize("username1, password, username2", [
    ("jacek", "123", "jabzek"),
    ("John321", "!DSgdfkmap", "John12345!")])


def test_create_profile_user_exists(mock_environment, monkeypatch, username1, password, username2, tmp_path):
    users_file = mock_environment
    inputs = [username1, username2, password, password]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    (tmp_path / f"{username1}.json").touch()
    result = create_profile(users_file)
    assert_profiles_creation(result, username2, password, users_file)


@pytest.mark.parametrize("username, password1, password2, password", [
    ("jacek", "123", "321", "123"),
    ("William654$", "gkap3vmASB", "Gkap3vmASB", "h2VA!#FDDDA")])


def test_create_profile_different_passwords(mock_environment, monkeypatch, username, password1, password2, password):
    users_file = mock_environment
    inputs = [username, password1, password2, password, password]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    result = create_profile(users_file)
    assert_profiles_creation(result, username, password, users_file)


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


def assert_profiles_deleting(user_data, user_file, users_file):
    with open(users_file, "r") as f:
        users_data = json.load(f)
    
    assert user_data not in users_data
    assert not user_file.exists()


@pytest.mark.parametrize("username, password, decision", [
    ("jacek", "123", "yes"),
    ("leon4jds", "F@BafvLOP", "yes"),
    ("ann531", "hobbit123", "yes"),
    ("johnus941", "arZWksPP", "yes")])


def test_delete_profile_everything_correct(mock_environment, monkeypatch, tmp_path, username, password, decision):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    user_file = tmp_path / f"{username}.json"
    user_data = {"username": username, "password": password, "file": str(user_file)}
    inputs = [password, decision, decision]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    _, _ = delete_profile(user_data, users_file)
    assert_profiles_deleting(user_data, user_file, users_file)


@pytest.mark.parametrize("username, password1, password2, decision", [
    ("jacek", "321", "123", "yes"),
    ("leon4jds", "Fsckj123lv", "F@BafvLOP", "yes"),
    ("ann531", "vader123", "hobbit123", "yes"),
    ("johnus941", "njzpjnDGK", "arZWksPP", "yes")])


def test_delete_profile_wrong_password(mock_environment, monkeypatch, tmp_path, username, password1, password2, decision):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    user_file = tmp_path / f"{username}.json"
    user_data = {"username": username, "password": password2, "file": str(user_file)}
    inputs = [password1, password2, decision, decision]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    _, _ = delete_profile(user_data, users_file)
    assert_profiles_deleting(user_data, user_file, users_file)


def assert_profiles_deleting_cancel(user_data, user_file, users_file):
    with open(users_file, "r") as f:
        users_data = json.load(f)
    
    assert user_data in users_data
    assert user_file.exists()


@pytest.mark.parametrize("username, password, decision", [
    ("jacek", "123", "return"),
    ("leon4jds", "F@BafvLOP", "return"),
    ("ann531", "hobbit123", "return"),
    ("johnus941", "arZWksPP", "return")])


def test_delete_profile_cancel1(mock_environment, monkeypatch, tmp_path, username, password, decision):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    user_file = tmp_path / f"{username}.json"
    user_data = {"username": username, "password": password, "file": str(user_file)}
    inputs = [decision]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    _, _ = delete_profile(user_data, users_file)
    assert_profiles_deleting_cancel(user_data, user_file, users_file)


@pytest.mark.parametrize("username, password, decision", [
    ("jacek", "123", "no"),
    ("leon4jds", "F@BafvLOP", "no"),
    ("ann531", "hobbit123", "no"),
    ("johnus941", "arZWksPP", "no")])


def test_delete_profile_cancel2(mock_environment, monkeypatch, tmp_path, username, password, decision):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    user_file = tmp_path / f"{username}.json"
    user_data = {"username": username, "password": password, "file": str(user_file)}
    inputs = [password, decision]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    _, _ = delete_profile(user_data, users_file)
    assert_profiles_deleting_cancel(user_data, user_file, users_file)


def assert_change_password(users_file, username, old_password, new_password, cancel):
    with open(users_file, "r") as f:
        users_data = json.load(f)
    
    for user in users_data:
        if user["username"] == username:
            if not cancel:
                assert user["password"] == new_password
            else:
                assert user["password"] == old_password
            break


@pytest.mark.parametrize("username, password1, password2", [
    ("jacek", "123", "321"),
    ("leon4jds", "F@BafvLOP", "SBakkds"),
    ("ann531", "hobbit123", "vader123"),
    ("johnus941", "arZWksPP", "Blaju3")])


def test_change_password_everything_correct(mock_environment, monkeypatch, tmp_path, username, password1, password2):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    inputs = [password1, password2, password2]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    change_password(users_file, username, password1)
    assert_change_password(users_file, username, password1, password2, cancel=False)


@pytest.mark.parametrize("username, wrong_password, password1, password2", [
    ("jacek", "fnjs", "123", "321"),
    ("leon4jds", "SJFj13gd", "F@BafvLOP", "SBakkds"),
    ("ann531", "GDjahhpi32", "hobbit123", "vader123"),
    ("johnus941", "mkmsafk@#%$", "arZWksPP", "Blaju3")])


def test_change_password_wrong_old_password(mock_environment, monkeypatch, tmp_path, username, wrong_password, password1, password2):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    inputs = [wrong_password, password1, password2, password2]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    change_password(users_file, username, password1)
    assert_change_password(users_file, username, password1, password2, cancel=False)


@pytest.mark.parametrize("username, password1, password2", [
    ("jacek", "123", "321"),
    ("leon4jds", "F@BafvLOP", "SBakkds"),
    ("ann531", "hobbit123", "vader123"),
    ("johnus941", "arZWksPP", "Blaju3")])


def test_change_password_same_password(mock_environment, monkeypatch, tmp_path, username, password1, password2):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    inputs = [password1, password1, password2, password2]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    change_password(users_file, username, password1)
    assert_change_password(users_file, username, password1, password2, cancel=False)


@pytest.mark.parametrize("username, wrong_password, password1, password2", [
    ("jacek", "fnjs", "123", "321"),
    ("leon4jds", "SJFj13gd", "F@BafvLOP", "SBakkds"),
    ("ann531", "GDjahhpi32", "hobbit123", "vader123"),
    ("johnus941", "mkmsafk@#%$", "arZWksPP", "Blaju3")])


def test_change_password_bad_repetition(mock_environment, monkeypatch, tmp_path, username, wrong_password, password1, password2):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    inputs = [password1, password2, wrong_password, password2, password2]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    change_password(users_file, username, password1)
    assert_change_password(users_file, username, password1, password2, cancel=False)


@pytest.mark.parametrize("username, password, decision", [
    ("jacek", "123", "return"),
    ("leon4jds", "F@BafvLOP", "return"),
    ("ann531", "hobbit123", "return"),
    ("johnus941", "arZWksPP", "return")])


def test_change_password_cancel(mock_environment, monkeypatch, tmp_path, username, password, decision):
    users_file = mock_environment
    saving_data_to_file(users_file, tmp_path)
    inputs = [decision]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    change_password(users_file, username, password)
    assert_change_password(users_file, username, password, None, cancel=True)

