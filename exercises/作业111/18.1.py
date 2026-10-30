import time
def insert_time(func):              # ① 收函数
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args,*kwargs)
        end = time.time()
        print(end-start)
        return result
    return wrapper


def a():
    time.sleep(1)
    print("wan")

insert_time(a())