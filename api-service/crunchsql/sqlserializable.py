from crunchsql import SqlProperty


class SqlSerializable:
    """
    Provide child classes an interface
    for representing themselves in a key-value
    structure compatible with SQL queries such
    as INSERT INTO table (param1, param2) VALUES (x, y)
    - by calling the __format__ using format() on the
    object.

    SqlProperties can be added by adding function
    references to the dictionary '_sql_property'
    which the __format__ will traverse and bind the
    property by name and value upon concatenating the
    formatted SQL representation of the object.
    """

    def __init__(self):
        self.id_autoincrement = False
        self.sql_properties: dict[str: SqlProperty] = {}
        self.id: int = int()
        self.columns: tuple[str] = tuple()
        self.values: tuple[str] = tuple()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(size: {self.__sizeof__()}b" \
               f", columns: {self.columns}, values: {self.values}"

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value
        self.sql_properties["id"] = SqlProperty(value=self.id, pos=0)

    @property
    def columns(self) -> tuple:
        self.__update_columns()
        return self._columns

    @columns.setter
    def columns(self, value: tuple):
        self._columns = value

    @property
    def values(self) -> tuple:
        self.__update_values()
        return self._values

    @values.setter
    def values(self, value: tuple):
        self.__update_columns()
        for column, val in zip(self._columns, value):
            setattr(self, column, val)
        self._values = value

    def __update_columns(self) -> None:
        """
        Updates the 'columns' tuple property to
        accurately mirror the configurations of
        the sql_properties dict configuiration,
        containing the name of all the properties
        that are created. The tuple is ordered
        by the 'pos' property on the SqlProperty
        which is the value of the given column.
        This is so, to mimic the return order from
        the database.

        Sorts the keys in sql_properties by defined 'pos' property.
        Truncate the 'id' property if it is autoincrement in the database,
        rendering it redundant in the insert query.
        """
        if self.id_autoincrement:
            columns = [i for i in self.sql_properties.keys() if i != "id"]
        else:
            columns = self.sql_properties.keys()

        self._columns = tuple(sorted(columns, key=lambda i: self.sql_properties[i].pos))

    def __update_values(self) -> None:
        if self.id_autoincrement:
            self.sql_properties.pop("id")
        properties = sorted(self.sql_properties.values(), key=lambda i: i.pos)
        self._values = tuple([i.value for i in properties])
