from os import getenv
from models.tables import Device, User
from crunchsql import SqlCommand, SqlCondition, SqlQuery, SqlSerializable
from exceptions.queryexception import DeviceAlreadyEnrolledException
from exceptions.queryexception import DeviceAlreadyExistsException
from exceptions.queryexception import UsernameTakenException


class ModelsByPropertyGenerator(SqlQuery):
    table_name = str()
    model = SqlSerializable

    def __call__(self, where=SqlCondition()) -> list[SqlSerializable]:
        cmd = SqlCommand()
        cmd.select = "*"
        cmd.select_from = getenv(self.__class__.table_name)
        if where: cmd.where = where
        cmd.columns = self.__class__.model().columns

        for db_data in self.execute_sql(cmd):
            obj = self.__class__.model()
            obj.values = db_data
            yield obj


class DeviceFinder(ModelsByPropertyGenerator):

    table_name = "DevicesTable"
    model = Device


class UserFinder(ModelsByPropertyGenerator):

    table_name = "UsersTable"
    model = User


class UserRegistrator(SqlQuery):

    def __call__(self, new_user: User):
        """
        Register a new user by creating a new
        entry in the database in the 'users'
        table.
        @param new_user:
            User to add in the database.
        @return:
            True, if succeeded
        @raise:
            UsernameTakenException
        """
        user_finder = UserFinder()

        for _ in user_finder(SqlCondition(username=new_user.username)):
            raise UsernameTakenException

        new_user.id_autoincrement = True
        cmd = SqlCommand()
        cmd.insert_into = getenv("UsersTable")
        cmd.columns = new_user.columns
        cmd.values = new_user.values
        return super().execute_sql(cmd)


class DeviceRegistrator(SqlQuery):

    def __call__(self, new_device: Device):
        """
        Register a new device in the database.
        """
        device_finder = DeviceFinder()

        for _ in device_finder(SqlCondition(device_id=new_device.device_id)):
            raise DeviceAlreadyExistsException

        new_device.id_autoincrement = True
        cmd = SqlCommand()
        cmd.insert_into = getenv("DevicesTable")
        cmd.columns = new_device.columns
        cmd.values = new_device.values
        return super().execute_sql(cmd)


class DeviceEnroller(SqlQuery):
    """
    Update ownership of a device in the database
    using the models for these tables.

    :raise DeviceAlreadyEnrolledException:
        In case a device is encountered to already be
        enrolled with a user
    """

    def __call__(self, new_owner: User, device: Device):
        device_finder = DeviceFinder()

        # Check if device is already enrolled with a user
        for d in device_finder(SqlCondition(device_id=device.device_id)):
            if d.user_id is not None:
                raise DeviceAlreadyEnrolledException

        # Configure the inner command which isolates 'id' for the user
        find_user_cmd = SqlCommand()
        find_user_cmd.select = "id"
        find_user_cmd.select_from = getenv("UsersTable")
        find_user_cmd.where = SqlCondition(username=new_owner.username)

        # Configure the outer, wrapping command
        cmd = SqlCommand()
        cmd.update = getenv("DevicesTable")
        cmd.set = SqlCondition()
        cmd.set["user_id"] = find_user_cmd
        cmd.where = SqlCondition(device_id=device.device_id)

        return super().execute_sql(cmd)


class DeviceDisenroller(SqlQuery):
    """
    Disenroll the device from current owner,
    making the device available for enrollment
    for other users.
    """

    def __call__(self, device: Device):
        device_finder = DeviceFinder()
        cmd = SqlCommand()

        cmd.update = getenv("DevicesTable")
        cmd.set = SqlCondition(user_id=None)
        cmd.where = SqlCondition(device_id=device.device_id)

        for i in device_finder(where=SqlCondition(device_id=device.device_id)):
            if i: return SqlQuery.execute_sql(cmd)
