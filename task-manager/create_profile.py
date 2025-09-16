import json
from pathlib import Path

def get_file(name):
    main_folder = Path(__file__).resolve().parent.parent
    user_folder = main_folder / "user-data"
    file = user_folder / f"{name}.json"
    return file

    
def create_profile(users_file):
    print("Enter your login details to create a new profile.")
    while True:
        try:
            username = input("Username: ")
            user_file = get_file(username)
            if user_file.exists():
                raise FileExistsError
            break
        except FileExistsError:
            print("User already exists. Please choose a different username.")
    

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
        json.dump(users_data, f)      
    