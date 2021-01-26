from usermanager.user import User
from usermanager.password import Password
from sqlclient.sqlcommand import SqlCommand


class UserManager:
    """
    The UserManager class is an encapsualted
    manager object to provide the user with
    a one-stop object for the creation,
    read, update and deletion of user accounts.

    The UserManager class communicates with the
    database through the provided SqlCommands
    that are provided from the user.

    Users can be deserialized from an SQL database after
    instantiation and can be modified as the
    'User' object allows.
    """

    def __init__(self):
        self._sql_commands: dict[str: SqlCommand] = {}

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __iadd__(self, other: User):
        pass

    def new_user(self, username: str, email: str,
                 firstname: str, lastname: str,
                 password_plaintext: str) -> bool:
        """
        Creates a new user, if the username is vacant
        and complies with the limitations set.

        :param username:
            Username for the user
        :param email:
            Email for the user
        :param firstname:
            Firstname of the user
        :param lastname:
            Lastname of the user
        :param password_plaintext:
            Plain text password for the user
        :returns:
            bool, if user was created successfully
        :raises:
            UsernameIsTakenException: username already exists in the
            database
        """
        if not self._username_available(username):
            return False

        new_user = User(username, email, firstname, lastname)
        new_user.password = Password(password_plaintext)

        # TODO: Insert user to database
        self._sql_client.execute(self._sql_commands["add_user"](new_user))
        return True

    def delete_user(self, username: str) -> bool:
        """
        Deletes a user if available.
        :param username: username of user to delete, str
        :returns: bool, successful removal
        """
        try:
            pass
            # TODO: Delete user from database
        except KeyError:
            return False
        return True

    def _username_available(self, username: str) -> bool:
        """
        Checks whether a given username is available
        for claim.
        :param username: username to check, str
        :returns: bool, available or not
        """
        return not bool(self._username_user_map.get(username))