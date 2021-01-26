import uuid
from password import Password


class User:
    """
    This model represents a user, plain and
    simple.
    Password can be assigned but will be hashed
    upon assignment to the property. This way, the
    plaintext password is never stored and has a limited
    lifespan of the local scope of the parameter to the
    setter method.
    """

    def __init__(self, username: str, email: str,
                 firstname: str, lastname: str):
        self._username: str = username
        self._email: str = email
        self._firstname: str = firstname
        self._lastname: str = lastname
        self._password: Password = None
        self._uuid = str(uuid.uuid4())

    def __repr__(self) -> str:
        return f"User(size: {self.__sizeof__()}b, uuid: {self._uuid})"

    def __str__(self) -> str:
        return f"username: {self._username}, email: {self._email}, " \
               f"firstname: {self._firstname}, lastname: {self._lastname}"

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def firstname(self) -> str:
        return self._firstname

    @property
    def lastname(self) -> str:
        return self._lastname

    @property
    def password(self) -> Password:
        return self._password

    @property
    def uuid(self) -> str:
        return self._uuid

    @password.setter
    def password(self, password: Password) -> None:
        if not isinstance(password, Password):
            raise AttributeError("password must be of type <Password>")
        self._password = password
