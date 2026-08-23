class BaseModel:
    """Common behavior shared by all model/entity classes.

    Subclasses only need to define __init__ with their own fields;
    this base class takes care of turning a sqlite3.Row (or dict)
    into an instance, and gives every model a readable __repr__.
    """

    @classmethod
    def from_row(cls, row):
        """Build an instance from a sqlite3.Row / dict, or None."""
        if row is None:
            return None
        data = dict(row)
        return cls(**cls._map_row(data))

    @classmethod
    def _map_row(cls, data):
        """Override in subclasses if column names differ from field names."""
        return data

    def to_dict(self):
        return dict(self.__dict__)

    def __repr__(self):
        fields = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({fields})"
