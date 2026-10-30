def make_counter():
    counter = 0
    def new():
        nonlocal  counter
        counter += 1
        return counter
    return new

c1 = make_counter()
c2 = make_counter()
print(c1(), c1(), c2())



