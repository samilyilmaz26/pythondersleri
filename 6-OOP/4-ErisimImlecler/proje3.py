class Base:
       # private  data members
     
    __kkno = None
  
     # constructor
    def __init__(self, name, kkno):
           
           # public data members
           self.name = name
           self.__kkno = kkno
 
     # public member function     
    def   displaykkno(self):
           
           # accessing public data member
           print("kkno: ",  "*******" + str(self.__kkno)[8:10])
     
           # accessing public data member
           
 
# creating object of the class
obj = Base("Şamil", 1234567890)
 
# accessing public data member
print("Name: ", obj.name)
#print ("Kredi Kart No ", obj.__kkno)
# calling public member function of the class
obj.displaykkno()

class Customer(Base):
     
       # constructor
       def __init__(self, name, kkno):
                Customer.__init__(self, name, kkno)
cust = Base("Şamil Yılmaz", 1234567890)
print("Name: ", cust.name)
#print ("Kredi Kart No ", cust.__kkno)
cust.displaykkno() 