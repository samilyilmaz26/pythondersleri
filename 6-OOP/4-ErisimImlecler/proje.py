class Base:
      
     # constructor
     def __init__(self, name, kkno):
           
           # public data members
           self.name = name
           self.kkno = kkno
 
     # public member function     
     def displaykkno(self):
           
           # accessing public data member
           print("kkno: ", "******" + str(self.kkno)[8:10])
 
# creating object of the class
obj = Base("R2J", 1234567890)
 
# accessing public data member
print("Name: ", obj.name)
print ("Kredi Kart No ", obj.kkno)
# calling public member function of the class
obj.displaykkno()