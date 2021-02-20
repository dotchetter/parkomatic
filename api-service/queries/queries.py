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

    device_enroller = EnrollDevice()
    user_finder = GetUserByProperty()

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
        for _ in device_finder(SqlCondition(device_id=device.device_id)):
            raise DeviceAlreadyEnrolledException

        # Configure the inner command which isolates 'id' for the user
        find_user_cmd = SqlCommand()
        find_user_cmd.select = "id"
        find_user_cmd.select_from = getenv("UsersTable")
        find_user_cmd.where = SqlCondition(email=new_owner.username)

        # Configure the outer, wrapping command
        cmd = SqlCommand()
        cmd.update = getenv("DevicesTable")
        cmd.set = SqlCondition()
        cmd.set["user_id"] = find_user_cmd
        cmd.where = SqlCondition(device_id=device.device_id)

        return super().execute_sql(cmd)
    delete_user_cmd.delete_from = getenv("UsersTable")
    delete_user_cmd.where = SqlConditon()
    delete_user_cmd.where["email"] = my_user.email

    print(delete_user_cmd)

    update_device_owner_cmd = SqlCommand()
    update_device_owner_cmd.update = getenv("DevicesTable")
    update_device_owner_cmd.set = SqlConditon()
    update_device_owner_cmd.set["user_id"] = SqlCommand(select="id",
                                                        select_from=getenv("UsersTable"),
                                                        where=user_where)
    update_device_owner_cmd.where = SqlConditon()
    update_device_owner_cmd.where["device_id"] = my_device.device_id

    print(update_device_owner_cmd)

    db = DbManager(getenv("SqlConnectionString"))
    """