import threading
import time


def worker(sing):
    print(sing)
    time.sleep(0.5)
    print(sing)

t1 = threading.Thread(target=worker, args=("212",))
t2 = threading.Thread(target=worker, args=("1212",))
t1.start()
t2.start()
t1.join()
t2.join()