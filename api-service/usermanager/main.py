from usermanager.user import User
from password import Password


if __name__ == "__main__":
    print()

    username = input("username: ")
    email = input("email: ")
    firstname = input("firstname: ")
    lastname = input("lastname: ")
    password = input("password: ")

    my_user = User(username, email, firstname, lastname)
    my_password = Password(password)
    my_user.password = my_password

    print(f"Your password: {my_user.password}")
    print(f"repr of password: {repr(my_user.password)}")

    print(f"Your user: {my_user}")
    print(f"repr of user: {repr(my_user)}")

    while True:
        if input("Test your password: ") == my_user.password:
            print("Correct password")
        else:
            print("Incorrect password")