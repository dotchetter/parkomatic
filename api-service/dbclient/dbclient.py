from models.password import Password
from models.tables import Device, Message, User
from models.sqlcommand import SqlCommand
from dotenv import load_dotenv
from os import getenv
import pyodbc


def execute_sql_command(cmd: SqlCommand) -> list:
    """

    """
    output: list

    with pyodbc.connect(getenv("SqlConnectionString")) as client:
        cursor = client.cursor()
        cursor.execute(str(cmd))
        output = [i for i in cursor]
        client.commit()

    return output


if __name__ == "__main__":
    load_dotenv()

    new_user = User()
    new_user.username = "foo"
    new_user.email = "foo@gmail.com"
    new_user.password = Password("foobar")

    insert_cmd = SqlCommand()
    insert_cmd.insert_into = getenv("UsersTable")
    insert_cmd.columns = new_user.columns
    insert_cmd.values = new_user.values

    user_columns_cmd = SqlCommand()
    user_columns_cmd.select = "COLUMN_NAME"
    user_columns_cmd.select_from = getenv("SchemaColumns")
    user_columns_cmd.where = {"TABLE_NAME": "'users'"}

    print(user_columns_cmd)

    get_devices_cmd = SqlCommand()
    get_devices_cmd.select = "*"
    get_devices_cmd.select_from = getenv("DevicesTable")

    print(execute_sql_command(user_columns_cmd))