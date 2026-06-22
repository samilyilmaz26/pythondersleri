def add(a,b):
    return a + b
def sub(a,b):
    return a-b
def mult(a,b):
    return a * b
def div(a,b):
    return a / b
def calc(f1,f2,f3,f4,opkod): # Tanımladığımız 4 fonksiyonu da argüman  .
    if (opkod == "+"):
        print(f1(3,4))
    elif (opkod == "-"):
        print(f2(3,4))
    elif (opkod == "*"):
        print(f3(3,4))
    elif (opkod== "/"):
        print(f4(3,4))
        
    else:
        print("invalid operation ..")
print(calc(add,sub,mult,div ,"*"))
