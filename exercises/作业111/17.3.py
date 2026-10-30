import threading

cond = threading.Condition()
items = []

def producer():
    for i in range(3):
        with cond:
            items.append(i)
            print(f"生产{i}")
            cond.notify()

def consumer():
    for i in range(3):
        with cond:
            while not items:
                cond.wait()
            print(f"消费{items.pop()}")

t1 = threading.Thread(target=consumer)
t2 = threading.Thread(target=producer)
t1.start(); t2.start()
t1.join();  t2.join()