from enum import Enum, auto


class SqlCommandType(Enum):
    SELECT = auto()
    INSERT = auto()


class SqlCommand:
    """
    The SqlCommand class is an object oriented
    approach to the traditional string-oriented
    SQL command.

    With SqlCommand objects, the user can abstract
    many considerations that can cause syntax errors
    and other problems when interacting with a database.
    """
    def __init__(self, table: str, command_type: SqlCommandType):
        self._table: str = table
        self._columns: tuple[str] = "*"
        self._command_type = command_type
        self._order_by: str = str()
        self._select_from: str = str()
        self._values: tuple[str] = tuple()

        self._types = {SqlCommandType.SELECT: self.__select_query,
                       SqlCommandType.INSERT: self.__insert_query}

    def __repr__(self):
        """
        Represents itself in pure SQL, concatenating
        all the parameters and configs set in the
        instance
        """
        return self._types[self._command_type]()

    @property
    def columns(self):
        if self._command_type == SqlCommandType.INSERT and self._columns == "*":
            raise UserWarning("'columns' property not set. This is required for INSERT commands.")
        return self._columns

    @columns.setter
    def columns(self, value: tuple[str]):
        self._columns = value

    @property
    def table(self) -> tuple[str]:
        return self._table

    @table.setter
    def table(self, value: tuple[str]):
        self._table = value

    @property
    def values(self) -> tuple[str]:
        return self._values

    @values.setter
    def values(self, value: tuple[str]):
        self._values = value

    def __select_query(self) -> str:
        return f"SELECT {self.columns} FROM {self.table}"

    def __insert_query(self) -> str:
        return f"INSERT INTO {self.table} {self.columns} VALUES {self.values}"


if __name__ == "__main__":

    cmd = SqlCommand(table="parkomatic-db.dbo.messages",
                     command_type=SqlCommandType.INSERT)

    cmd.columns = ("lat", "lon")
    cmd.values = ("59.11232", "18.13982")

    print(cmd)