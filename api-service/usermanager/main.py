from usermanager.user import User
from password import Password


if __name__ == "__main__":
    print()

    password = Password(input("Enter password: "))

    print(f"Your password: \n{repr(password)}")

    while True:
        if input("Test your password: ") == password:
            print("Correct password")
        else:
            print("Incorrect password")