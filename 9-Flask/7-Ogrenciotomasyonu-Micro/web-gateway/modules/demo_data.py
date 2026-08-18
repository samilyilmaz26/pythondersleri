class DemoData:
    """Small OOP stand-in for the old modules/var.py sample data.

    Kept as its own class so the /degiskenler demo page still shows
    a few example Jinja variables, now sourced from an object instead
    of loose module-level functions. Has no DB dependency, so it stays
    in the gateway rather than becoming its own microservice.
    """

    def __init__(self):
        self.isim = "Ali"
        self.yas = 25
        self.user = {"isim": "Ali", "yas": 25}
        self.userlist = [
            {"isim": "Ali", "yas": 25},
            {"isim": "Veli", "yas": 30},
            {"isim": "Ayşe", "yas": 20},
        ]

    def as_template_context(self):
        return {
            "isim": self.isim,
            "yas": self.yas,
            "user": self.user,
            "userlist": self.userlist,
        }
