import uuid
from models.password import Password
from crunchsql import SqlSerializable
from crunchsql import SqlProperty


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
        self.sql_properties["device_id"] = SqlProperty(value=self.device_id, pos=1)

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

    def __init__(self, id: int = None,
                 device_id: str = None,
                 user_id: int = None):
        super().__init__()
        self.id = id
        self.user_id = user_id
        self.device_id = device_id

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, value: str):
        self._user_id = value
        self.sql_properties["user_id"] = SqlProperty(self.user_id, pos=1)

    @property
    def device_id(self) -> str:
        return self._device_id

    @device_id.setter
    def device_id(self, value: str):
        self._device_id = value
        self.sql_properties["device_id"] = SqlProperty(self.device_id, pos=2)


class User(SqlSerializable):
    """
    This model represents a user,
    plain and simple.
    """

    # noinspection PyTypeChecker
    def __init__(self, id: int = None,
                 user_id: str = None,
                 username: str = None,
                 hashed_password: str = None,
                 email: str = None,
                 password_salt: str = None):
        super().__init__()

        self.id = id
        self.username = username
        self.email = email
        self.user_id = user_id if user_id else str(uuid.uuid4())

        if hashed_password and password_salt:
            self.password = Password(hashed_password=hashed_password,
                                     salt_hex=password_salt)
        else:
            self.password = Password()

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value
        self.sql_properties["username"] = SqlProperty(value=self.username,
                                                      pos=2)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value
        self.sql_properties["email"] = SqlProperty(value=self.email,
                                                   pos=4)

    @property
    def password(self) -> Password:
        return self._password

    @password.setter
    def password(self, password: Password) -> None:
        if not isinstance(password, Password) and isinstance(password, str):
            password = Password(hashed_password=password)

        self._password = password
        self.sql_properties["password"] = SqlProperty(value=str(self.password),
                                                      pos=3)
        self.sql_properties["salt"] = SqlProperty(value=self.password.salt,
                                                  pos=5)

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, value: str):
        self._user_id = value
        self.sql_properties["user_id"] = SqlProperty(value=self.user_id,
                                                     pos=1)

    @property
    def salt(self):
        return self.password.salt

    @salt.setter
    def salt(self, value: str):
        self.password.salt = value
