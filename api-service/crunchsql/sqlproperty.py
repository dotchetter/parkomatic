from typing import Any
from dataclasses import dataclass


@dataclass
class SqlProperty:
    """
    The SqlProperty class represents
    a property, or column, in a table
    from the database. The SqlProperty
    acts as a binder between the name of
    a column on a table in the SqlDatabase
    which a field in a class corresponds
    with.

    For easy serialization and de-serialization
    of objects, the order of which values
    are entered are not trivial since the return
    from a SQL query usually yields tuples
    of values. To match a field with a certain
    order in a tuple, this class aims to
    offer an easy interface for column name and
    field binding.
    """

    value: Any
    pos: int
