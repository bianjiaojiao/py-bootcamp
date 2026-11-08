---
title: 迭代器与 enumerate
category: 进阶
keywords: [迭代器, iterator, iter, next, 可迭代对象, enumerate, StopIteration, for]
dates: [2026-10-18]
---

# 迭代器与 enumerate

> 一句话：**迭代器是一个可以记住遍历位置的对象**——只能往前走、不能后退，走完就空了；`enumerate` 是"既要值又要下标"的标准解法。

## 1. 迭代器是什么

> 「迭代器是一个可以记住遍历位置的对象。」

迭代器对象从集合的第一个元素开始访问，直到所有元素被访问完为止。

**两个特点**：

- 只能**往前**，不能**后退**
- 用 `iter()` 把可迭代对象变成迭代器；用 `next()` 取下一个元素

```python
nums = [1, 2, 3]
it = iter(nums)        # list → 迭代器

print(next(it))        # 1
print(next(it))        # 2
print(next(it))        # 3
print(next(it))        # 抛异常 StopIteration（没有第 4 个了）
```

字符串、列表、元组都可以用来创建迭代器；迭代器既可以用 `for` 遍历，也可以用 `next()` 逐个取。

## 2. ⚠️ 不可逆 + 会被"吃掉"（重点）

这是最容易踩的坑，也是今天的重点笔记：

```python
it = iter([1, 2, 3])
next(it)               # 1 —— 这个元素已经被消耗掉了
list(it)               # [2, 3]  ← 少了 1！不是 [1, 2, 3]
```

再取一次就彻底空了：

```python
it = iter([1, 2, 3])
print(list(it))        # [1, 2, 3]
print(list(it))        # []   ← 已耗尽，再也回不去
```

**为什么重要**：

- 迭代器**不可逆**——像游戏里"用掉的补给"，取走就没了
- 同一个迭代器被"用掉一部分"后，转成列表**也会少掉那部分**
- 想重复遍历 → 每次重新 `iter()`，或者直接用列表

## 3. `for` 循环本质就是迭代器

```python
for fruit in ["苹果", "香蕉"]:
    print(fruit)
```

大致等价于：

```python
it = iter(["苹果", "香蕉"])
while True:
    try:
        fruit = next(it)
    except StopIteration:
        break
    print(fruit)
```

> 这就是为什么生成器和迭代器能直接放进 `for`——`for` 只要求"可迭代"，不要求"能随机访问"。

## 4. `enumerate`：既要值又要下标

```python
fruits = ['苹果', '香蕉', '橘子']
for i, fruit in enumerate(fruits):
    print(i, fruit)
```

输出：

```text
0 苹果
1 香蕉
2 橘子
```

`enumerate(可迭代对象)` 返回一个**（下标，元素）**的迭代器，省去你自己维护一个计数变量的麻烦：

```python
# ❌ 老写法
i = 0
for fruit in fruits:
    print(i, fruit)
    i += 1

# ✅ 新写法
for i, fruit in enumerate(fruits):
    print(i, fruit)

# 还可以指定起始下标
for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)      # 1 苹果 / 2 香蕉 / 3 橘子
```

## 5. `for` 是最标准、最常用的迭代方式

> `for` 循环就是 Python 里最标准、最常用的迭代方式。

```python
for x in [1, 2, 3]:
    print(x)
```

比 `while` + `next()` 更常用的原因：

- 自动处理 `StopIteration`，不用手写 `try/except`
- 代码短、意图清楚
- 任何「可迭代对象」都能直接用：列表、元组、字符串、字典、文件、生成器

```python
for ch in "abc":            # 字符串
for k in {"a": 1}:          # 字典（遍历 key）
for line in open("f.txt"):  # 文件（逐行）
```

## ⚠️ 易错点速记

1. 迭代器**只能用一次**，耗尽后再取是空的（`list(it)` 第二次是 `[]`）
2. `next(it)` 取走的元素**不会回来**，转列表也会少
3. 迭代器**不能后退**，需要回退就重新 `iter()`
4. 取完还调 `next()` 会抛 `StopIteration`，`for` 会自动处理，手写 `while` 要自己 `try/except`
5. 拿下标别自己维护计数器，用 `enumerate(seq, start=1)`

## 🔗 关联

- 生成器（`yield` 也是迭代器）→ [08-生成器](08-生成器.md)
- 列表与元组 → [03-列表与元组](03-列表与元组.md)
- 原始截图 → [source/2026-10-18/A.md](../source/2026-10-18/A.md)（图 image31、image32）
- 今日手写要点：「迭代可以用来取补给（游戏），因为它不可逆，且调用一次后原本的 iter() 即使转化为列表也会少那一个」

---

## 补充：`zip` 并行遍历（2026-11-08）

**一句话**：同时遍历两个（或多个）列表，一对一对取。

```python
names = ["小明", "小红", "小刚"]
scores = [90, 85, 77]

for name, score in zip(names, scores):
    print(name, score)
# 小明 90
# 小红 85
# 小刚 77
```

### 和 `enumerate` 的区别

| 函数 | 给什么 | 什么时候用 |
| --- | --- | --- |
| `enumerate(列表)` | 下标 + 元素 | 需要"第几个" |
| `zip(列表1, 列表2)` | 两个列表的对应元素 | 需要"配对" |

### 三个常用变体

```python
# ① 转字典（最常用）
d = dict(zip(names, scores))     # {"小明": 90, "小红": 85, ...}

# ② 三个列表一起
for a, b, c in zip(l1, l2, l3): ...

# ③ 矩阵转置
rows = [(1, 2), (3, 4)]
cols = list(zip(*rows))          # [(1, 3), (2, 4)]
```

### 坑

```python
zip([1, 2, 3], ["a", "b"])       # 只配对 2 个，第三个丢弃（按短的截断）
```

**长度不等时静默截断，不报错**——想严格一致就自己先检查 `len`。

### 在哪见过

`course-rag/rag/store.py:82`：

```python
Chunk(text=str(t), source=str(s))
for t, s in zip(data["texts"], data["sources"])
```
