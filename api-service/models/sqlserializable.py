

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

    @property
    def columns(self) -> str:
        return f"({str(', ').join(self.sql_properties.keys())})"

    @columns.setter
    def columns(self, value: tuple):
        self._columns = value

    @property
    def values(self) -> tuple:
        return tuple(self.sql_properties.values())

    @values.setter
    def values(self, value: tuple):
        self._values = value
