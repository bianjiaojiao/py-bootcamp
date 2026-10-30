class dog:
    species="犬科"
    count =0
    def __init__(self,name):
        self.name = name
        dog.count+=1
a=dog("a")
b=dog("b")
print(a.name,b.name)
print(dog.count)