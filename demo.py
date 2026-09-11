class calculator():
    def two_no_result(fun):
        def wrapper(self,a=11.0,b=2.0):
            if not isinstance(a,float) or not isinstance(b,float):
                raise TypeError("Both are float value")

            result=fun(self,a,b)
            return float(result)
        return wrapper

    


    @two_no_result
    def add(self,a=10.0,b=2.0):
        return a+b

c=calculator()
print(c.add())
# print(c.add(10,2))    