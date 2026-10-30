import threading

counter = 0
lock = threading.Lock()

def add_100():
    global counter
    for i in range(10000):
        with lock:
            counter += 1



threads = []

# 2. 循环 4 次
for _ in range(4):

    t = threading.Thread(target=add_100)
    threads.append(t)

for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)