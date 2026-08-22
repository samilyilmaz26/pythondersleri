from models.base_model import BaseModel


class Student(BaseModel):
    """Represents a row of the students table."""

    def __init__(self, id=None, name="", surname=None, street=None, number=None, cityid=None, departmentid=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.street = street
        self.number = number
        self.cityid = cityid
        self.departmentid = departmentid
