from time import sleep
from action_on_profiles import create_profile, get_file, log_into_profile, delete_profile, change_password

# To do: add task, remove task, show tasks (with filtres), password change, 
# task status change, task edit, task history, 


def managing_account(user_data, users_file):
    username = user_data["username"]
    password = user_data["password"]
    print(f"Welcome {username}!!!")
    
    while True: 
        user_action = input("What do you want to do: ").strip()
        match user_action:
            case "quit":
                exit = True
                print("Exiting from Task Manager.")
                break
            case "logout":
                print("Logging out of your profile.")
                exit = False
                break
            case "delete":
                delete, exit = delete_profile(user_data, users_file)
                if not delete:
                    continue
                break   
            case "password":
                user_data, password = change_password(users_file, username, password)
    return exit


def action(users_file):
    print("Do you want to create a new profile or choose from existing ones?")
    while True:
        decision = input("Choice: ")
        if decision == "create":
            user_data = create_profile(users_file)
            break
        elif decision == "choose":
            user_data = log_into_profile(users_file)
            break
        else:
            print("Try again.")
    exit_program = managing_account(user_data, users_file)
    return exit_program


def main():
    print("Welcome in your Task Manager!")
    sleep(1)
    users_file = get_file("users")
    
    if not users_file.exists():
        print("Let's create first profile.")
        sleep(1)
        user_data = create_profile(users_file)
        exit_program = managing_account(user_data, users_file)
    else:
        exit_program = action(users_file)
    
    while not exit_program:
        exit_program = action(users_file)


if __name__ == "__main__":
    main()