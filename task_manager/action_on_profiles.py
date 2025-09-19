import json
from pathlib import Path

def get_file(name):
    main_folder = Path(__file__).resolve().parent.parent
    user_folder = main_folder / "user_data"
    user_folder.mkdir(exist_ok=True)
    file = user_folder / f"{name}.json"
    return file

    
def create_profile(users_file):
    print("Enter your login details to create a new profile.")
    while True:
        try:
            username = input("Username: ").strip()
            if username == "" or len(username) < 3:
                raise NameError
            user_file = get_file(username)
            if user_file.exists():
                raise FileExistsError
            break
        except FileExistsError:
            print("User already exists. Please choose a different username.")
        except NameError:
            print("Username must be at least 3 characters long")

    while True:
        password = input("Password: ")
        confirm_password = input("Confirm password: ")
        if password == confirm_password:
            break
        else:
            print("Passwords do not match. Please try again.")
        
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
    
    print("Profile has been created.")
    return user_data 


def choose_profile(users_file):
    print("Choose one profile from the following.")
    with open(users_file, "r") as f:
        profile_list = json.load(f)
    profile_names = []
    
    for user in profile_list:
        profile_names.append(user["username"])
    print(" ".join(profile_names))
    
    while True:
        try:
            profile = input("Choice: ")
            if profile not in profile_names:
                raise NameError
            break
        except NameError:
            print(f"{profile} does not exist. Try again.")
    