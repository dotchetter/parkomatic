from user import User


class UserManager:
    """
    The UserManager class is an encapsualted
    manager object to provide the user with
    a one-stop object for the creation,
    read, update and deletion of user accounts.

    The UserManager class communicates with the
    database through the provided SqlCommands
    that are provided from the user.

    Users are read from the database upon
    instantiation and can be modified as the
    'User' object allows.
    """

    def __init__(self):
        self._user_lookup = dict[str: User]

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __add__(self, other):
        pass

    def __iadd__(self, other):
        pass

    def new_user(self, username: str, email: str,
                 firstname: str, lastname: str):
        pass