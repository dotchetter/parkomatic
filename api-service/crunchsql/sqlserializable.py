from models.sqlproperty import SqlProperty


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
    def columns(self) -> str:
        self.__update_columns()
        return f"({str(', ').join(self._columns)})"

    @columns.setter
    def columns(self, value: tuple):
        self._columns = value

    @property
    def values(self) -> tuple:
        return self._values

    @values.setter
    def values(self, value: tuple):
        self.__update_columns()
        for column, val in zip(self.columns, value):
            setattr(self, column, val)
        self._values = value

    def __update_columns(self) -> None:
        """
        Updates the 'columns' tuple property to
        accurately mirror the configurations of
        the sql_properties dict configuiration,
        containing the name of all the properties
        that are created. The tuple is ordered
        by the 'pos'property on the SqlProperty
        which is the value of the given column.
        This is so, to mimic thereturn order from
        the database.
        """
        columns = list(self.sql_properties.keys())
        # Sorts the keys in sql_properties by defined 'pos' property
        self._columns = sorted(columns, key=lambda i: self.sql_properties[i].pos)
