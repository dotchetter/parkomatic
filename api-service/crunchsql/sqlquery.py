from os import getenv
import pyodbc
from abc import ABC, abstractmethod
from models.sqlcommand import SqlCommand


class SqlQuery(ABC):
    """
    Abstract class for subclassing
    when creating pre-made query objects
    that serves as factories or inserters
    to and from a database.

    A SqlQuery object instance is designed
    to work with the various Sql- models
    and provide a very convenient and
    modular interface to perform queries
    toward an SQL database.
    """
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    @staticmethod
    def execute_sql(query: SqlCommand):
        """
        Performs SQL string commands
        using ODBC with pyodbc targeting
        Microsoft SQL databases.

        Requires the property
        "SqlConnectionString" to be set
        in the local .env file for means
        to connec to the server.

        Returns list of tuples containing
        the result of given query.

        :param query:
            raw SQL command string
        :returns list:
            list with tuples of returned
            data form the query
        :raises:
            None, but will display errors
            by enclosing messages in the
            return list.
        """
        with pyodbc.connect(getenv("SqlConnectionString")) as client:
            cursor = client.cursor()
            cursor.execute(str(query))

            if query.insert_into or query.update:
                client.commit()
                output = True
            else:
                output = [i for i in cursor]

            client.commit()
        return output
