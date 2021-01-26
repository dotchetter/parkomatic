import os
import pyodbc
from sqlcommand import SqlCommand
from dotenv import load_dotenv


class SqlClient:
    """
    SQL Server connection client class.

    The SqlClient object acts as a connection
    handler between the user and a Microsoft SQL
    server, performing queries using 'SqlCommand'
    object instances, representing the queries.
    """

    def __init__(self):
        load_dotenv()
        self._db_connection = pyodbc.connect(os.getenv("SqlConnectionString"))

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def execute(self, command: SqlCommand):
        """
        Executes the SqlCommand object that was
        passed, in the connected database.
        """
        _cursor = self._db_connection.cursor()
        _cursor.execute(command)