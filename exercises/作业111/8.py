def squares(n):
    for i in range(1,n+1):
        yield i * i


# ================= 验证 1：用 for 遍历打印 =================
print("--- 第一次遍历（for循环）---")
for num in squares(5):
    print(num, end=" ")
print("\n")

# ================= 验证 2：生成器只能迭代一次 =================
print("--- 验证生成器是一次性耗材 ---")
gen = squares(5)  # 创建了一个生成器对象

# 第一次转换成 list
first_list = list(gen)
print(f"第一次 list()：{first_list}")

# 第二次转换成 list（注意：用的还是刚才那个 gen）
second_list = list(gen)
print(f"第二次 list()：{second_list}")

# 验证结果
if first_list and not second_list:
    print("✅ 验证成功：同一个生成器第二次迭代是空的（它被抽干了）！")