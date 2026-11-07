---
title: functools（lru_cache 缓存 / partial 偏函数）
category: 工程
keywords: [functools, lru_cache, partial, 缓存, 装饰器, 偏函数, 提速]
dates: [2026-11-07]
---

# functools（lru_cache 缓存 / partial 偏函数）

> 一句话：**`lru_cache` 让重复计算变免费，`partial` 给函数"预填"一个参数。**

---

# 一、`lru_cache` —— 记住算过的结果

## 为什么需要

```python
def slow_square(n):
    time.sleep(1)          # 假装很慢（比如要调模型 / 跑复杂计算）
    return n * n

slow_square(5)     # 等 1 秒
slow_square(5)     # 又等 1 秒 ← 明明答案一样，白等
```

**同样的输入，答案是一样的。为什么不记住？**

## 加一行就解决

```python
from functools import lru_cache

@lru_cache
def slow_square(n):
    time.sleep(1)
    return n * n

slow_square(5)     # 等 1 秒（真算）
slow_square(5)     # 立刻返回（直接用缓存）
slow_square(5)     # 立刻返回
```

**第一次算，之后全白拿。**

## 怎么验证真的缓存了

用计数器：

```python
from functools import lru_cache

calls = 0                      # 记录"真算了几次"

@lru_cache
def slow_square(n):
    global calls
    calls = calls + 1          # 只有真算才 +1
    return n * n

slow_square(5)
slow_square(5)
slow_square(5)
print(calls)      # 1  ← 调用 3 次，只真算了 1 次
```

## `lru` 是什么意思

**L**east **R**ecently **U**sed —— 最近最少使用。

缓存不能无限大（内存有限），所以要淘汰老的。默认存 **128 个**。

```python
@lru_cache(maxsize=32)     # 只存 32 个结果
def f(n): ...
```

`maxsize=None` = 无限存（小心内存）。

## ⚠️ 坑 1：参数必须能哈希

```python
@lru_cache
def f(items):              # ❌ 传列表会报错
    ...

f([1, 2, 3])               # TypeError: unhashable type: 'list'
f((1, 2, 3))               # ✅ tuple 可以
```

**原因**：缓存是个字典，键必须是不可变的（字符串/数字/tuple）。

## ⚠️ 坑 2：`@lru_cache` 必须写在最外层装饰器

```python
@lru_cache
@另一个装饰器
def f(): ...
```

顺序写反了，缓存会缓存"另一个装饰器的结果"，可能不是你想要的。

## ⚠️ 坑 3：结果变了它不知道

```python
@lru_cache
def get_config():
    return open("config.txt").read()

# 你改了 config.txt
get_config()      # 还是旧内容！因为缓存了
```

**解决**：`get_config.cache_clear()`

## 在项目里什么时候用

| 场景 | 用不用 |
| --- | --- |
| 读固定的配置文件 | ✅ 用 |
| 查数据库的固定字典表 | ✅ 用 |
| 加载 embedding 模型 | ✅ **非常适合**（加载一次要 2 秒） |
| 每次输入都不同的问答 | ❌ 没用（永远不命中） |

---

# 二、`partial` —— 给函数预填参数

## 为什么需要

```python
def pow(base, exp):
    return base ** exp

pow(2, 10)    # 1024
pow(3, 10)    # 59049
pow(4, 10)    # 1048576  ← 每次都要写 10
```

**如果我总是要"某个数的 10 次方"，能不能预先填好 10？**

## 一行解决

```python
from functools import partial

ten_power = partial(pow, exp=10)      # 把 exp 固定成 10

ten_power(2)      # 1024
ten_power(3)      # 59049
ten_power(4)      # 1048576
```

**`partial(函数, 固定参数)` → 返回一个"新函数"，那个参数不用再传了。**

## 按位置固定 vs 按名字固定

```python
# 按名字固定（推荐，清楚）
square = partial(pow, exp=2)
square(6)        # 36

# 按位置固定（固定第一个参数）
add = lambda a, b: a + b
add10 = partial(add, 10)
add10(5)         # 15   ← 等价 add(10, 5)
```

## 典型用途 1：给回调函数传参

```python
# 按钮点击时，想传"是哪个按钮"
def on_click(name, event):
    print("点了", name)

button1 = partial(on_click, "按钮1")     # 少传一个参数
button2 = partial(on_click, "按钮2")
```

## 典型用途 2：简化常用调用

```python
import json

# 每次都写 ensure_ascii=False 很烦
save_json = partial(json.dumps, ensure_ascii=False, indent=2)

save_json({"name": "边角"})
# '{\n  "name": "边角"\n}'
```

## 典型用途 3：LangChain / API 里固定参数

```python
# 项目里常见：固定模型名、温度
from functools import partial

def call_llm(model, temperature, prompt):
    ...

fast = partial(call_llm, "deepseek-chat", 0)      # 结果稳定
creative = partial(call_llm, "deepseek-chat", 1)  # 更发散
```

---

# 两个对比总结

| | `lru_cache` | `partial` |
| --- | --- | --- |
| 干什么 | **记住结果**（同样的输入不再算） | **预填参数**（少传一个） |
| 用在哪 | 装饰器 `@lru_cache` | 函数 `partial(f, x)` |
| 解决什么 | **重复计算太慢** | **每次都要传同样的参数太烦** |
| 注意 | 参数必须可哈希 | 别和"默认参数"搞混 |

## `partial` 和默认参数的区别

```python
# 默认参数
def pow2(n, exp=10):
    return n ** exp

# partial
ten = partial(pow, exp=10)
```

**都能达到效果。区别**：

| | 默认参数 | partial |
| --- | --- | --- |
| 谁写的 | 你写函数时定的 | 调用方定的 |
| 能用几次 | 一次定义，固定 | 可以造出很多变体 |

**别人写的函数**（比如 `pow`、`json.dumps`）你改不了默认参数，这时用 `partial`。

---

## 速记卡

```
lru_cache   @lru_cache 加在函数上，重复调用直接拿缓存
            maxsize 控制存几个，cache_clear() 清空
            参数必须不可变（tuple 行，list 不行）

partial     partial(函数, 固定参数) -> 新函数
            适合给别人写的函数"预填参数"
```

---

## 🔗 相关

- 装饰器：[06-装饰器](06-装饰器.md)（如果你有这篇）
- 闭包：[18-闭包](18-闭包.md)（partial 本质是闭包）
- 语法体能：[03_语法体能3.py](../../../agent-lab/03-语法训练/03_语法体能3.py) 第 7、8 关
