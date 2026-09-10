class Calculator:

    def check_type(func):
        def wrapper(self, a, b):
            if not isinstance(a, float) or not isinstance(b, float):
                raise TypeError("Both numbers must be float")

            result = func(self, a, b)
            print("result_issss",result)
            return float(result)

        return wrapper

    @check_type
    def add(self, a, b):
        return a + b


c = Calculator()

print(c.add(10.0, 20.0))     # 30.0
print(c.add(5, 7))       # 12.0

# print(c.add(10.5, 20))   # TypeError