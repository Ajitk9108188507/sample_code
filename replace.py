class Demo:

    def duplicate_no(self):
        a = [1, 2, 3,5,5, 4, 5, 6, 8, 8]

        dup=[]
        for i in a:
           if a.count(i)>1 and i not in dup:
                dup.append(i)
        print(dup)    

        unique = [] 

        for i in a:
            if i not in unique:
                unique.append(i)
        print(unique)           

d = Demo()
d.duplicate_no()