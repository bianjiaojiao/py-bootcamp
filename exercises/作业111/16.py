def add(self):
    return f"{self.name}+1"
addd = type("addd",(object,),{"name":1,"age":2,"add":add})
a = addd()
print(a.add())