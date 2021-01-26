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

    # noinspection PyTypeChecker
    def __init__(self, username: str, email: str):
        self._username: str = username
        self._email: str = email
        self._password: Password = None
        self._user_id = str(uuid.uuid4())

    def __repr__(self) -> str:
        return f"User(size: {self.__sizeof__()}b, user_id: {self._user_id})"

    def __str__(self) -> str:
        return f"username: {self._username}, email: {self._email}"

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> Password:
        return self._password

    @property
    def user_id(self) -> str:
        return self._user_id

    @password.setter
    def password(self, password: Password) -> None:
        if not isinstance(password, Password):
            raise AttributeError("password must be of type <Password>")
        self._password = password


if __name__ == "__main__":
    user = User("dotchetter", "dotchetter@protonmail.ch")
    user.password = Password("password123")

    print(user.__dict__)