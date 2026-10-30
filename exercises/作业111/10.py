import random

num = random.randint(1,100)
tryies = 0

while True:
    try:
        a = int(input())
    except ValueError:
        print("请输入数字")
        continue
    except KeyboardInterrupt:  # 👈 接住 Ctrl+C 中断
        print("\n游戏已手动退出。")
        break
    if a > num:
        print("大了")
        tryies += 1

    elif a < num:
        print("小了")
        tryies += 1
    else:
        print(f"猜了{tryies+1}次")
        if tryies > 10:
            print("cai")
        elif tryies < 10:
            print("good")
        break