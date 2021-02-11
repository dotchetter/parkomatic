from models.password import Password
from models.sqlserializable import SqlSerializable
from os import getenv
from models.sqlquery import SqlQuery
from models.tables import Device, Message, User
from models.sqlcommand import SqlCommand, SqlCondition


class GetUserByProperty(SqlQuery):
    """
    Returns User() model instances serialized
    from data returned upon given query from
    the SQL database.
    """

    def __call__(self, condition: SqlCondition) -> list[User]:

        output = []
        cmd = SqlCommand()
        cmd.select = "*"
        cmd.select_from = getenv("UsersTable")
        cmd.where = condition
        cmd.columns = User().columns

        for db_user_data in SqlQuery.execute_sql(cmd):
            user = User()
            user.values = db_user_data
            output.append(user)
        return output


class EnrollDevice(SqlQuery):
    """
    Update ownership of a device in the database
    using the models for these tables.
    """

    def __call__(self, user: User, device: Device):

        check_device_owner = SqlCommand()
        check_device_owner.select = "*"
        check_device_owner.select_from = getenv("DevicesTable")
        check_device_owner.where = SqlCondition(device_id=device.device_id)

        """
        cmd = SqlCommand()
        cmd.update = getenv("DevicesTable")
        cmd.set = SqlCondition(user_id=SqlCommand(select="id",
                                                  select_from=getenv("Userstable"),
                                                  where=SqlCondition(email=user.email)))
        cmd.where = SqlCondition(device_id=device.device_id)
        """


if __name__ == "__main__":

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