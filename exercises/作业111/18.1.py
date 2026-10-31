import time
def insert_time(func):              # ① 收函数
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args,**kwargs)
        result = func(*args,**kwargs)
        end = time.time()
        print(end-start)
        return result
    return wrapper

@insert_time
def a():
    time.sleep(1)
    print("wan")


a()