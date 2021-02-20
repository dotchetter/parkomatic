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

    condition = SqlCondition()
    condition["username"] = "simon"
    condition["or"] = True
    condition["username"] = "anton"

    matched = user_finder(condition)
    print(*matched, sep="\n")

    """
    my_user = User()
    my_user.username = "simon"
    my_user.email = "dotchetter@protonmail.ch"

    my_device = Device()
    my_device.device_id = "55b076a9-3efc-4593-9975-25f8048fa56e"

    anton = User()
    anton.email = "annoiot19@gmail.com"

    antons_device = Device()
    antons_device.device_id = "2ce2fa33-4abc-4a77-bc3e-aa50b3e2ec88"

    user_where = SqlConditon()
    user_where["user_id"] = my_user.user_id

    delete_user_cmd = SqlCommand()
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