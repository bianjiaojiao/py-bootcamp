---
title: collections 与 heapq（常用容器速查）
category: 工程
keywords: [defaultdict, deque, Counter, heapq, nlargest, 容器, 标准库]
dates: [2026-11-08]
---

# collections 与 heapq（常用容器速查）

> 这类是**标准库 API**，不是语法。**知道名字 + 查一次文档**就够，不用背。
> 但下面这 4 个用得极频繁，值得混个脸熟。

---

# 一、`defaultdict` —— 计数不用写 if

## 问题

```python
d = {}
for ch in "aab":
    if ch not in d:          # ← 每次都要先判断
        d[ch] = 0
    d[ch] = d[ch] + 1
```

## 解决

```python
from collections import defaultdict

d = defaultdict(int)         # 缺失的键默认给 int() = 0
for ch in "aab":
    d[ch] = d[ch] + 1        # 直接加，不用判断

print(dict(d))               # {'a': 2, 'b': 1}
```

## 默认值可以是什么

| 写法 | 缺失时给 | 用在 |
| --- | --- | --- |
| `defaultdict(int)` | `0` | 计数 |
| `defaultdict(list)` | `[]` | 分组（把同类元素塞进列表） |
| `defaultdict(set)` | `set()` | 去重分组 |
| `defaultdict(lambda: "未知")` | `"未知"` | 自定义默认值 |

## 分组例子（最常用）

```python
from collections import defaultdict

words = ["apple", "avocado", "banana", "blueberry"]
groups = defaultdict(list)
for w in words:
    groups[w[0]].append(w)      # 按首字母分组

print(dict(groups))
# {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry']}
```

**没有 defaultdict 就得写 `if w[0] not in groups: groups[w[0]] = []`。**

---

# 二、`deque(maxlen=n)` —— 只保留最后 n 个

## 问题

"只保留最近 3 次的结果"——用 list 要自己删：

```python
history = []
for x in items:
    history.append(x)
    if len(history) > 3:
        history.pop(0)        # 删最老的，但 pop(0) 很慢（O(n)）
```

## 解决

```python
from collections import deque

q = deque(maxlen=3)           # 最多存 3 个
for x in [1, 2, 3, 4, 5]:
    q.append(x)               # 塞第 4 个时，第 1 个自动消失

print(list(q))                # [3, 4, 5]
```

**塞超了就自动挤掉最老的，不用你管。**

## `deque` 和 `list` 的区别

| 操作 | list | deque |
| --- | --- | --- |
| 尾部加 | `append` O(1) | `append` O(1) |
| **头部加/删** | `insert(0, x)` / `pop(0)` **O(n)** | `appendleft` / `popleft` **O(1)** |
| 随机访问 `[i]` | O(1) | O(n)（慢） |

**结论**：需要"两头进出"就用 deque，需要"按下标取"就用 list。

## 典型用途

```python
# ① 滑动窗口（比如"最近 5 条日志"）
recent = deque(maxlen=5)

# ② 队列（先进先出）
q = deque()
q.append("任务1")
q.append("任务2")
q.popleft()      # "任务1"

# ③ 栈（先进后出）
stack = deque()
stack.append(1)
stack.pop()      # 1
```

---

# 三、`Counter` —— 专做计数

你已经有（04 字典、07 词频统计）。快速回顾：

```python
from collections import Counter

c = Counter("aabbc")
print(c)                 # Counter({'a': 2, 'b': 2, 'c': 1})
print(c.most_common(2))  # [('a', 2), ('b', 2)]   ← 最常见的前 2 个
print(c["a"])            # 2
print(c["z"])            # 0    ← 不存在的键返回 0，不报错
```

**`most_common(n)` 就是 Top-N 计数的标准写法。**

---

# 四、`heapq` —— 取 Top-N 而不用全排序

## 问题

"10000 个数里取最大 3 个"——用 `sort` 要排全部：

```python
nums = [...]                 # 10000 个
top = sorted(nums, reverse=True)[:3]    # 排完 10000 个才拿 3 个
```

**时间复杂度 O(n log n)，明明只需要 3 个。**

## 解决

```python
import heapq

top = heapq.nlargest(3, nums)     # O(n log 3)，快很多
```

## 4 个常用函数

| 函数 | 干什么 | 例子 |
| --- | --- | --- |
| `nlargest(n, 列表)` | 取前 n **大**，从大到小 | `nlargest(3, [5,1,9,3,7])` → `[9, 7, 5]` |
| `nsmallest(n, 列表)` | 取前 n **小**，从小到大 | `nsmallest(2, [5,1,9])` → `[1, 5]` |
| `nlargest(n, 列表, key=...)` | 按某个字段取 | `nlargest(2, people, key=lambda p: p["age"])` |
| `heappush` / `heappop` | 维护一个"堆"（随时取最小） | 见下 |

## 带 key 的用法（更像真实场景）

```python
people = [
    {"name": "小明", "score": 88},
    {"name": "小红", "score": 95},
    {"name": "小刚", "score": 72},
]

best = heapq.nlargest(2, people, key=lambda p: p["score"])
# [{'name': '小红', 'score': 95}, {'name': '小明', 'score': 88}]
```

**和 `sorted(..., key=...)[:2]` 效果一样，但更快。**

## 什么时候需要 `heappush` / `heappop`

需要"**动态维护**一个优先队列"时（不断有新数据进来，随时要拿最小的）：

```python
import heapq

heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)

heapq.heappop(heap)      # 1   ← 每次拿到最小的
heapq.heappop(heap)      # 3
```

**堆 = 一个永远能 O(log n) 拿到最小值的列表。**

---

# 什么时候用哪个（决策表）

| 你要做什么 | 用什么 |
| --- | --- |
| 计数（每个出现几次） | `Counter` 或 `defaultdict(int)` |
| 分组（按某个字段归类） | `defaultdict(list)` |
| 只保留最近 n 个 | `deque(maxlen=n)` |
| 队列/栈（两头进出） | `deque` |
| 取前 n 大/小 | `heapq.nlargest` / `nsmallest` |
| 全排序后取 | `sorted(...)` |
| 随机按下标访问 | `list`（不要用 deque） |

---

# 在 RAG 项目里的对应

| 场景 | 用什么 |
| --- | --- |
| 统计哪些词出现最多 | `Counter` |
| 检索结果取前 3（只取不排全） | `heapq.nlargest(3, ...)` 或 `sorted(...)[:3]` |
| 保留最近 5 轮对话 | `deque(maxlen=5)` |
| 按笔记名分组统计块数 | `defaultdict(list)` |

> **注意**：`course-rag` 现在用的是 `np.argsort(scores)[::-1][:k]`（numpy 全排序）。
> 501 块时很快；10 万块时换成 `heapq.nlargest` 更合适。**知道有替代方案就行。**

---

# 速记卡

```
defaultdict(int)    计数不用判断
defaultdict(list)   分组不用判断
deque(maxlen=n)     只留最后 n 个，自动挤掉老的
deque               两头进出 O(1)（list 的 pop(0) 是 O(n)）
Counter             计数 + most_common(n)
heapq.nlargest(n,x) 取前 n 大，不用全排序
heapq.nsmallest     取前 n 小
```

---

## 🔗 相关

- 字典：[04-字典](04-字典.md)
- 去重与词频统计：[07-去重与词频统计](07-去重与词频统计.md)
- 列表与元组：[03-列表与元组](03-列表与元组.md)
- 语法体能：[04_语法体能4.py](../../../agent-lab/03-语法训练/04_语法体能4.py) 第 6~10 关
