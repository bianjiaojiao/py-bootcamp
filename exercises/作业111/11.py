def divide(a,b):
    return a // b, a % b
def add_item(item,bucket=None):
    if bucket is None :
        bucket = []
    bucket.append(item)
    return bucket
people = [
    {"name": "小明", "age": 20},
    {"name": "小红", "age": 19},
    {"name": "小刚", "age": 25},
]
# 按 age 从小到大
print(sorted(people,key = lambda x:x['age']))
q, r = divide(17, 5)
print("商:", q, "余数:", r)        # 3 2

a = add_item(1)
b = add_item(2)
print(a, b)                        # [1] [2]   ← 关键验证
