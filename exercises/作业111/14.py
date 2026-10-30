from enum import Enum,IntEnum
class Status(Enum):
    PENDING = 1
    RUNNING = 2
    DONE =3
print(Status.PENDING.name)
print(Status.PENDING.value)


class im(IntEnum):
    a = 1
    b=2
print(im.b>im.a)