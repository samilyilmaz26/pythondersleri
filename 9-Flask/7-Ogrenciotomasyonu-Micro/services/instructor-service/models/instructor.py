from models.student import Student


class Instructor(Student):
    """Represents a row of the Egitmen table (an instructor).

    An instructor is a student plus a title (unvan), so it reuses
    Student's name/department/address fields and full_name/full_address
    properties instead of redefining them.
    """

    def __init__(self, id=None, ad="", soyad="", bolumid=None, bolumad=None,
                 mahalle="", cadde="", kapino="", city="",
                 unvanid=None, unvanad=None):
        super().__init__(
            id=id, ad=ad, soyad=soyad, bolumid=bolumid, bolumad=bolumad,
            mahalle=mahalle, cadde=cadde, kapino=kapino, city=city,
        )
        # unvanad (title name) is owned by title-service; this service
        # only ever stores/returns unvanid, never joins it in.
        self.unvanid = unvanid
        self.unvanad = unvanad
