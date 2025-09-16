from time import sleep
from pathlib import Path
from create_profile import create_profile, get_file

def menu():
    pass


def main():
    def choose_profiles(users_file):
        print("Do you want to create a new profile or choose from existing ones?")
        while True:
            decision = input("Choice: ")
            if decision == "create":
                create_profile(users_file)
                menu()
            elif decision == "choose":
                break
            else:
                print("Try again")
    
    print("Welcome in your Task Manager!")
    sleep(2)
    users_file = get_file("users")
    if not users_file.exists():
        print("Let's create first profile")
        sleep(1)
        create_profile(users_file)
        menu()
    else:
        choose_profiles(users_file)







if __name__ == "__main__":
    main()