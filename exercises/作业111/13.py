class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y



    def __eq__(self, other):
        if not isinstance(other,Point):
            return False
        else:
            if self.x == other.x and self.y ==other.y:
                return True
            else:
                return False




    def __hash__(self):
        return hash((self.x, self.y))


print(Point(1,2) == Point(1,2))
print(len({Point(1,2), Point(1,2)}))
