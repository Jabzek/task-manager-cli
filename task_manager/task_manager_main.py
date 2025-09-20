from time import sleep
from action_on_profiles import create_profile, get_file, log_into_profile

def main():
    def action(users_file):
        print("Do you want to create a new profile or choose from existing ones?")
        while True:
            decision = input("Choice: ")
            if decision == "create":
                user_data = create_profile(users_file)
            elif decision == "choose":
                log_into_profile(users_file)
            else:
                print("Try again")
    
    print("Welcome in your Task Manager!")
    sleep(1)
    users_file = get_file("users")
    if not users_file.exists():
        print("Let's create first profile")
        sleep(1)
        user_data = create_profile(users_file)
    else:
        action(users_file)

if __name__ == "__main__":
    main()