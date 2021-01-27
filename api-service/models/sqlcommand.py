def serialize_dict(source: dict[str: str], delimiter=", ") -> str:
    """
        Serializes a dictionary with K:V structure
        to SQL compatible format, that is:
        "X = Y AND Z = A AND [...]"
        """
    output = []
    for key, value in source.items():
        if key.lower() == "and" and value is True:
            output.append("AND")
        elif key.lower() == "or" and value is True:
            output.append("OR")
        else:
            output.append(f"{key} = {value}")
    return delimiter.join(output)


class SqlCommand:
    """
    The SqlCommand class is an object oriented
    approach to the traditional string-oriented
    SQL command.

    With SqlCommand objects, the user can abstract
    many considerations that can cause syntax errors
    and other problems when interacting with a database.

    Complex queries such as WHERE with 'AND' and 'OR'
    statements, 'TOP' and joins make the abstractions
    easy to build with.
    """

    def __init__(self):
        self.select: str = str()
        self.select_from: str = str()
        self.columns: tuple[str] = tuple()
        self.where: dict[str: str] = {}
        self.inner_join: str = str()
        self.outer_join: str = str()
        self.left_join: str = str()
        self.right_join: str = str()
        self.full_join: str = str()
        self.order_by: str = str()
        self.insert_into: str = str()
        self.on: dict[str: str] = {}
        self.asc: bool = False
        self.desc: bool = False
        self.top: bool = False
        self.values: list[str] = []

    def __repr__(self):
        """
        Represents itself in pure SQL, concatenating
        all the parameters and configs set in the
        instance
        """
        return self.format_as_sql()

    def format_as_sql(self):
        output: list = []

        if self.select:
            output.append("SELECT")
            if not self.top and not self.select_from:
                raise AttributeError(
                    "Column(s) missing for FROM statement: 'select_from'")

            if self.top:
                output.append(f"({self.top}")
            else:
                output.append(f"{self.select} FROM {self.select_from}")

            if self.where:
                output.append(f"WHERE {self.where}")

            if self.inner_join or self.left_join or self.right_join or self.full_join:
                if not self.on:
                    raise AttributeError(
                        "Inner join requires the ON condition: 'on'")

                if self.inner_join:
                    output.append(f"INNER JOIN {self.inner_join}")
                elif self.full_join:
                    output.append(f"FULL OUTER JOIN {self.full_join}")
                elif self.right_join:
                    output.append(f"RIGHT JOIN {self.right_join}")
                elif self.left_join:
                    output.append(f"LEFT JOIN {self.left_join}")

                output.append(f"ON {self.on}")

            if self.order_by:
                output.append(f"ORDER BY {self.order_by}")
                if self.asc:
                    output.append("ASC")
                elif self.desc:
                    output.append("DESC")

        elif self.insert_into:
            if not self.columns:
                raise AttributeError ("Columns missing for the INSERT statement")
            output.append(f"INSERT INTO {self.insert_into} {self.columns} VALUES {self.values}")

        return " ".join(output)

    @property
    def select(self):
        return self._select

    @select.setter
    def select(self, value):
        if isinstance(value, tuple) or isinstance(value, list):
            value = ", ".join(value)
        self._select = value

    @property
    def select_from(self):
        return self._select_from

    @select_from.setter
    def select_from(self, value):
        if isinstance(value, tuple) or isinstance(value, list):
            value = ", ".join(value)
        self._select_from = value

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value

    @property
    def where(self):
        return self._where

    @where.setter
    def where(self, value: dict):
        if not isinstance(value, dict):
            raise AttributeError(
                "The WHERE condition must be dict as they are key-value pairs")
        self._where = serialize_dict(value, delimiter=" ")

    @property
    def inner_join(self):
        return self._inner_join

    @inner_join.setter
    def inner_join(self, value):
        self._inner_join = value

    @property
    def outer_join(self):
        return self._outer_join

    @outer_join.setter
    def outer_join(self, value):
        self._outer_join = value

    @property
    def left_join(self):
        return self._left_join

    @left_join.setter
    def left_join(self, value):
        self._left_join = value

    @property
    def right_join(self):
        return self._right_join

    @right_join.setter
    def right_join(self, value):
        self._right_join = value

    @property
    def full_join(self):
        return self._full_join

    @full_join.setter
    def full_join(self, value):
        self._full_join = value

    @property
    def order_by(self):
        return self._order_by

    @order_by.setter
    def order_by(self, value):
        if isinstance(value, tuple) or isinstance(value, list):
            value = ", ".join(value)
        self._order_by = value

    @property
    def insert_into(self):
        return self._insert_into

    @insert_into.setter
    def insert_into(self, value):
        self._insert_into = value

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, value):
        if not isinstance(value, dict):
            raise AttributeError(
                "The ON condition must be dict as they are key-value pairs")
        self._on = serialize_dict(value)

    @property
    def asc(self):
        return self._asc

    @asc.setter
    def asc(self, value):
        self._asc = value

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, value):
        self._desc = value

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        self._top = value

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = []

        for i in value:
            if isinstance(i, SqlCommand):
                self._values.append(f"({i})")
            else:
                self._values.append(i)

        self._values = tuple(self._values)


if __name__ == "__main__":
    get_device_id = SqlCommand()
    get_device_id.select = "id"
    get_device_id.select_from = "devices"
    get_device_id.where = {"device_id": "device_id_here"}

    insert_message = SqlCommand()
    insert_message.insert_into = "users"
    insert_message.columns = (user.columns)
    insert_message.values = (user.values)

    for i in dir(insert_message):
        if getattr(insert_message, i):
            print(i, getattr(insert_message, i))