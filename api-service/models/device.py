from models.sqlserializable import SqlSerializable


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
