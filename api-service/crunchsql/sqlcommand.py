import warnings
from typing import Any


class SqlCondition:
    """
    The SqlCondition class is an object
    designed to represent a WHERE, SET
    or other 'x = y' statement in SQL
    queries, where it is created and
    constructed in a dict-like manner.

    The SqlContidion class however,
    supports duplicate key occurances
    which is its primary strength.

    It also represents itself post-
    instantiation in a correct SQL
    syntax to be used within a SQL query.
    """

    def __init__(self, **kwargs):
        self._keys = []
        self._values = []
        self._content = []

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def __repr__(self):
        return str(" ").join(self._content)

    def __setitem__(self, key, value):
        if value is None: value = "NULL"
        self._keys.append(key)
        self._values.append(value)

        if key.lower().strip() == "and" and value is True:
            self._content.append("AND")
        elif key.lower().strip() == "or" and value is True:
            self._content.append("OR")
        elif isinstance(value, SqlCommand):
            self._content.append(f"{key} = ({value})")
        else:
            value = f"'{value}'" if value != "NULL" else value
            self._content.append(f"{key} = {value}")

    def __bool__(self):
        """
        Returns True if any conditions are
        stored in the instance, otherwise
        False.
        """
        return True if repr(self) else False


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
    def __init__(self, **kwargs):
        self.update: str = str()
        self.select: str = str()
        self.delete_from: str = str()
        self.select_from: str = str()
        self.columns: tuple[str] = tuple()
        self.where = SqlCondition()
        self.set = SqlCondition()
        self.inner_join: str = str()
        self.outer_join: str = str()
        self.left_join: str = str()
        self.right_join: str = str()
        self.full_join: str = str()
        self.order_by: str = str()
        self.insert_into: str = str()
        self.on = SqlCondition()
        self.asc: bool = False
        self.desc: bool = False
        self.top: bool = False
        self.values: list[str] = []

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        """
        Represents itself in pure SQL, concatenating
        all the parameters and configs set in the
        instance
        """
        return self.format_as_sql()

    def __str__(self):
        """
        Represents itself in pure SQL, concatenating
        all the parameters and configs set in the
        instance
        """
        return self.__repr__()

    def format_as_sql(self) -> str:
        """
        Structure a string containing the
        statement based on the provided logic
        using the different property methods
        in the class.
        :returns str:
            Represenation of all configurations in SQL syntax
        """
        output: list = []

        if self.delete_from:
            output.append(f"DELETE FROM {self.delete_from}")
            if not self.where:
                warnings.warn("WARNING: WHERE clause omitted. This will cause "
                              "the DELETE statement to affect ALL matching "
                              "records resulting in the query. ")
            else:
                output.append(f"WHERE {self.where}")
        if self.update:
            if not self.set:
                raise AttributeError("key-value pair missing for "
                                     "SET statement: 'SET x = y'")
            output.append(f"UPDATE {self.update} SET {self.set}")
            if not self.where:
                warnings.warn("WARNING: WHERE clause omitted. This will cause "
                              "the UPDATE statement to affect ALL matching "
                              "records resulting in the query. ")
            else:
                output.append(f"WHERE {self.where}")
        elif self.select:
            if not self.top and not self.select_from:
                raise AttributeError(
                    "Column(s) missing for FROM statement: 'select_from'")
            output.append("SELECT")
            if self.top:
                output.append(
                    f"{self.select} ({self.top}) {', '.join(self.columns)} "
                    f"FROM {self.select_from}")
            else:
                output.append(f"{self.select} FROM {self.select_from}")
            if self.where:
                output.append(f"WHERE {self.where}")
            if self.inner_join or self.left_join or self.right_join or self.full_join:
                if not self.on:
                    raise AttributeError("Inner join requires the ON "
                                         "condition: 'on'")
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
                raise AttributeError(
                    "Columns missing for the INSERT statement")
            output.append(
                f"INSERT INTO {self.insert_into} {self.columns} VALUES {self.values}")

        return " ".join(output)

    @property
    def update(self):
        return self._update

    @update.setter
    def update(self, value):
        self._update = value

    @property
    def set(self):
        return self._set

    @set.setter
    def set(self, value: SqlCondition):
        if not isinstance(value, SqlCondition):
            raise AttributeError("The SET condition must be "
                                 "of type 'SqlCondition'")
        self._set = value

    @property
    def select(self):
        return self._select

    @select.setter
    def select(self, value):
        if isinstance(value, tuple) or isinstance(value, list):
            value = ", ".join(value)
        self._select = value

    @property
    def delete_from(self):
        return self._delete_from

    @delete_from.setter
    def delete_from(self, value):
        self._delete_from = value

    @property
    def select_from(self):
        return self._select_from

    @select_from.setter
    def select_from(self, value):
        if isinstance(value, tuple) or isinstance(value, list):
            value = ", ".join(value)
        self._select_from = value

    @property
    def where(self):
        return self._where

    @where.setter
    def where(self, value: SqlCondition):
        if not isinstance(value, SqlCondition):
            raise AttributeError("The WHERE condition must be "
                                 "of type 'SqlCondition'")
        self._where = value

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
        if not isinstance(value, SqlCondition):
            raise AttributeError("The ON condition must be "
                                 "of type 'SqlCondition'")
        self._on = value

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
