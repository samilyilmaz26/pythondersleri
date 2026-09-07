from models.base_model import BaseModel


class StudentReadModel(BaseModel):
    """Denormalized student row used by the /students read path.

    Kept in sync with student-service, city-service and department-service
    via RabbitMQ events instead of being joined on every request.
    """

    def __init__(
        self,
        id=None,
        name="",
        surname=None,
        street=None,
        number=None,
        cityid=None,
        departmentid=None,
        cityname=None,
        departmentname=None,
    ):
        self.id = id
        self.name = name
        self.surname = surname
        self.street = street
        self.number = number
        self.cityid = cityid
        self.departmentid = departmentid
        self.cityname = cityname
        self.departmentname = departmentname
