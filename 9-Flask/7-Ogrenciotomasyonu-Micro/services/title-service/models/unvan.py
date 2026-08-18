from models.base_model import BaseModel


class Unvan(BaseModel):
    """Represents a row of the Unvan table (an instructor title)."""

    def __init__(self, id=None, unvanad=""):
        self.id = id
        self.unvanad = unvanad
