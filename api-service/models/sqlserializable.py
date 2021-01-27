

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
        self.sql_properties: dict[str: callable] = {}
        self._columns: tuple = tuple()
        self._values: tuple = tuple()

    def sql_serialize(self) -> None:
        """
        Updates the 'columns' and 'values' properties
        on self, for to more easily insert these
        parameters in Sql queries.

        :returns: None
        """
        self._columns = tuple(self.sql_properties.keys())
        self._values = tuple(self.sql_properties.values())

    @property
    def columns(self) -> tuple:
        return self._columns

    @columns.setter
    def columns(self, value: tuple):
        self._columns = value

    @property
    def values(self) -> tuple:
        return self._values

    @values.setter
    def values(self, value: tuple):
        self._values = value
