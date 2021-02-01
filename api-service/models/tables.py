import uuid
from models.password import Password
from models.sqlserializable import SqlSerializable


class Message(SqlSerializable):
    """
    Represents a message, produced
    by a device in the database.
    """

    def __init__(self):
        super().__init__()
        self.lat: str = str()
        self.lon: str = str()
        self.device_id: int = int()
        self.epochtime: int = int()

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = value
        self.sql_properties["lat"] = self._lat

    @property
    def lon(self):
        return self._lon

    @lon.setter
    def lon(self, value):
        self._lon = value
        self.sql_properties["lon"] = self._lon

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value
        self.sql_properties["device_id"] = self._device_id

    @property
    def epochtime(self):
        return self._epochtime

    @epochtime.setter
    def epochtime(self, value):
        self._epochtime = value
        self.sql_properties["epochtime"] = self._epochtime


class Device(SqlSerializable):
    """
    This model represents a device in
    the Parkomatic system platform.
    """

    def __init__(self):
        super().__init__()
        self.device_id: str = str()
        self.user_id: str = str()

    def __repr__(self):
        return f"Device(size: {self.__sizeof__()}b, device_id: {self._device_id})"

    @property
    def device_id(self) -> str:
        return self._device_id

    @device_id.setter
    def device_id(self, value: str):
        self._device_id = value
        self.sql_properties["device_id"] = self._device_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, value: str):
        self._user_id = value
        self.sql_properties["user_id"] = self._user_id


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
        self.sql_properties["password"] = str(self._password)
        self.sql_properties["salt"] = self._password.salt

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, value: str):
        self._user_id = value
        self.sql_properties["user_id"] = self._user_id
