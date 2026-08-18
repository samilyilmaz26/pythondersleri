from models.student import Student


class Instructor(Student):
    """View-model rebuilt from instructor-service's JSON responses.

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
        self.unvanid = unvanid
        self.unvanad = unvanad

    @classmethod
    def from_form(cls, form, id=None):
        return cls(
            id=id,
            ad=form.get("ad"),
            soyad=form.get("soyad"),
            bolumid=form.get("bolumid"),
            mahalle=form.get("mahalle"),
            cadde=form.get("cadde"),
            kapino=form.get("kapino"),
            city=form.get("city"),
            unvanid=form.get("unvanid"),
        )
