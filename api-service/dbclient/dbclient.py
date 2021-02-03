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


class DbClientABC:
    """
    SQL command executing abstract class.

    The DbClientABC base class allows subclasses
    to implement methods that perform certain
    actions relevant to the design of the
    app in question and the database in use.
    """
    @abc.abstractmethod
    def _execute_command(self, cmd: SqlCommand) -> Any:
        """
        Private method - meant for internal
        calls.

        Execute SqlCommand instances here.

        SqlCommand instances contain the
        queries in string format as they
        are called upon with either repr()
        or str().
        """
        pass


class DataLayer(DbClientABC):
    """
    Parkomatic backend database
    interaction object.

    Inherits from DbClient as to
    overload set methods
    """
    def __init__(self, dbconnectionstring: str):
        self._dbconnectionstring = dbconnectionstring

    def __repr__(self):
        pass

    def execute(self, cmd: SqlCommand) -> list[Any]:
        """
        Executes SqlCommand instances as
        str, or plain str queries by
        invoking the str() method on the
        cmd instance.

        pyodbc is used as to communicate with
        Microsoft Sql Server using ODBC 17.

        :param cmd:
            SqlCommand, or plain str query
        :returns:
            list, returned results from
            executed query.
        :raises:
            None, errors are passed but
            added to return output.
        """
        output: list

        with pyodbc.connect(self._dbconnectionstring) as client:
            cursor = client.cursor()
            cursor.execute(str(cmd))

            try:
                output = [i for i in cursor]
            except pyodbc.ProgrammingError as e:
                output = ["Errors occured:", e]
            client.commit()
        return output

    def add_query(self, cmd: SqlCommand, alias: str) -> None:
        """
        Allows users of an instance of this class
        to add executable commands with associated
        property name on the instance, dynamically.

        For instance, a command to add users can be
        constructed and then added to an instnace
        of this class as a way to call stored queries
        and update their values depending on use case.

        :param cmd:
            SqlCommand or str to store
        :param alias:
            str, alias which will be assigned using
            setattr
        :returns:
            None
        """
        #setattr(self, )
        pass
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