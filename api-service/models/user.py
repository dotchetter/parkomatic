import uuid
from password import Password
from models.sqlserializable import SqlSerializable


class User(SqlSerializable):
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
    def __init__(self, username: str = str(), email: str = str()):
        super().__init__()
        self.username: str = username
        self.email: str = email
        self.password: Password = Password()
        self.user_id = str(uuid.uuid4())

    def __repr__(self) -> str:
        return f"User(size: {self.__sizeof__()}b, user_id: {self._user_id})"

    def __str__(self) -> str:
        return f"username: {self._username}, email: {self._email}"

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value
        self.sql_properties["username"] = self._username

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value
        self.sql_properties["email"] = self._email

    @property
    def password(self) -> Password:
        return self._password

    @password.setter
    def password(self, password: Password) -> None:
        if not isinstance(password, Password):
            raise AttributeError("password must be of type <Password>")

        self._password = password
        self.sql_properties["password"] = self._password
        self.sql_properties["salt"] = self._password.salt

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, value: str):
        self._user_id = value
        self.sql_properties["user_id"] = self._user_id
