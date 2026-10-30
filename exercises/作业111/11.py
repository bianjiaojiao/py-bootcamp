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
