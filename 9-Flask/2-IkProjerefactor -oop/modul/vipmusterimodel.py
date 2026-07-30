# from Modules.musterimodul import PersonelModel

# import sqlite3
# class PersonelModel:
#     def __init__(self, id=None, ad=None, soyad=None, sehir=None):
#         self.id = id
#         self.ad = ad
#         self.soyad = soyad
#         self.sehir = sehir
#     @classmethod
#     def from_row(cls, row):
#         """Creates a PersonelModel instance from a sqlite3.Row object."""
#         return cls(
#             id=row['id'] if 'id' in row.keys() else None,
#             ad=row['ad'] if 'ad' in row.keys() else None,
#             soyad=row['soyad'] if 'soyad' in row.keys() else None,
#             sehir=row['sehir'] if 'sehir' in row.keys() else None,
#         )
# class PersonelRepository:
#     def __init__(self, db_name="IK.db"):
#         self.db_name = db_name

#     def get_all(self):
#         """Fetches all rows and maps them to a list of PersonelModel objects."""
#         with sqlite3.connect(self.db_name) as con:
#             con.row_factory = sqlite3.Row
#             cursor = con.cursor()
            
#             sorgu = 'SELECT * FROM personel'
#             rows = cursor.execute(sorgu).fetchall()
            
#             # Map every row dictionary into a PersonelModel object
#             return [PersonelModel.from_row(row) for row in rows]
# # Inside your Flask views/controllers:def perlist():
#     repo = PersonelRepository()
#     personel_objects = repo.get_all()  # Contains a list of PersonelModel instances
#     return render_template("personel/list.html", personel=personel_objects)

# The database columns are mapped directly into an explicit PersonelModel class. This encapsulates the data structure so your HTML templates can access properties using clean object syntax (e.g., {{ p.ad }} instead of {{ p['ad'] }}).
# If you want to expand this model, let me know if you would like to:

# * Add a save or update method to the model to handle inserts and edits directly.
# * Introduce a validation method inside the model to check if inputs like email or salary are formatted correctly.
# * See how to write the Jinja template code for this object-based list.


