# 1. Define the decorator function
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()  # This runs the original function
        print("Something is happening after the function is called.")
    return wrapper

# 2. Apply the decorator using the '@' symbol
@my_decorator
def say_hello():
    print("Hello!")

# 3. Call the decorated function
say_hello()
