import json
from pathlib import Path

def get_file(name):
    main_folder = Path(__file__).resolve().parent.parent
    user_folder = main_folder / "user_data"
    user_folder.mkdir(exist_ok=True)
    file = user_folder / f"{name}.json"
    return file

    
def saving_new_profile(users_file, user_file, username, password):
    user_file.touch()
    user_data = {"username": username,
                 "password": password,
                 "file": str(user_file)}

    if users_file.exists():
        with open(users_file, "r") as f:
            users_data = json.load(f)
    else:
        users_data = []
    users_data.append(user_data)
    
    with open(users_file, "w") as f:
        json.dump(users_data, f, indent=2)  

    return user_data


def create_profile(users_file):
    print("Enter your login details to create a new profile.")
    while True:
        try:
            username = input("Username: ").strip()
            if username == "" or len(username) < 3:
                raise ValueError
            user_file = get_file(username)
            if user_file.exists():
                raise FileExistsError
            break
        except FileExistsError:
            print("User already exists. Please choose a different username.")
        except ValueError:
            print("Username must be at least 3 characters long")

    while True:
        password = input("Password: ")
        confirm_password = input("Confirm password: ")
        if password == confirm_password:
            break
        else:
            print("Passwords do not match. Please try again.")
        
    user_data = saving_new_profile(users_file, user_file, username, password)

    print("Profile has been created.")
    return user_data 


def log_into_profile(users_file):
    print("Choose one profile from the following.")
    with open(users_file, "r") as f:
        profile_list = json.load(f)
    
    profile_names = []
    for user in profile_list:
        profile_names.append(user["username"])
    print(" ".join(profile_names))
    
    while True:
        try:
            username = input("User: ").strip()
            if username not in profile_names:
                raise ValueError
            
            for user in profile_list:
                if user["username"] == username:
                    user_data = user
                    break
            
            password = input("Password: ").strip()
            if password != user_data["password"]:
                raise PermissionError
            break
        except ValueError:
            print("User does not exist. Try again.")
        except PermissionError:
            print("Wrong password. Try again.")
    return user_data

def del_profile(users_file, user_data):
    file = user_data["file"]
    Path(file).unlink()
    
    with open(users_file, "r") as f:
        users_data = json.load(f)
    
    for user in users_data:
        if user_data["username"] == user["username"]:
            users_data.remove(user)
            break
    
    with open(users_file, "w") as f:
        json.dump(users_data, f, indent=2)


def delete_profile(user_data, users_file):
    print("Enter password to delete the account. If you enter \"return\" you will cancel your decision")
    while True:
        password = input("Password: ").strip()
        if password == user_data["password"]:
            break
        elif password == "return":
            return False, None 
        print("Try again.")
    
    print("Are you sure to delete your profile?")
    while True:
        decision = input("Decision: ")
        if decision == "no":
            return False, None
        elif decision == "yes":
            del_profile(users_file, user_data)
            break
        else:
            print("Try again.")
    
    print("Do you want close Task Manager?")
    while True:
        exit_decision = input("Decision: ").strip()
        if exit_decision == "no":
            return True, False
        elif exit_decision == "yes":
            return True, True
        else:
            print("Try again.")


def saving_new_password(users_file, username, new_password):
    with open(users_file, "r") as f:
        users_data = json.load(f)

    for user in users_data:
        if user["username"] == username:
            user["password"] = new_password
            break

    with open(users_file, "w") as f:
        json.dump(users_data, f, indent=2)

    return user


def change_password(users_file, user_data):
    print("Enter your password to change for a new one. If you enter \"return\" you will cancel your decision.")
    while True:
        old_password = input("Password: ").strip()
        if old_password == user_data["password"]:
            break
        elif old_password == "return":
            return user_data
        else:
            print("Try again.")
    
    print("Enter a new password.")
    while True:
        new_password = input("New password: ").strip()
        if new_password == old_password:
            print("You have entered your old password. Try again.")
            continue
        
        print("Repeat your new password.")
        repeat_password = input("New password: ").strip()
        if new_password != repeat_password:
            print("Passwords are not the same. Try again.")
            continue
        break
    
    user_data = saving_new_password(users_file, user_data["username"], new_password)
    print("Password has been changed.")
    return user_data
