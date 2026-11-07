---
title: asyncio 异步编程
category: 工程
keywords: [asyncio, async, await, 协程, 并发, gather, 事件循环, 阻塞]
dates: [2026-11-07]
---

# asyncio 异步编程

> 一句话：**等待的时候别干等，把时间让给别人。**
>
> 实测：3 个"等 1 秒"的任务，**同步 3.0 秒 → 异步 1.0 秒**。

---

## 为什么需要

```python
# 同步：一个一个来，干等
def task(n):
    time.sleep(1)      # 这 1 秒 CPU 什么都不干，纯浪费
    return n

task(1)   # 1 秒
task(2)   # 1 秒   ← 明明可以一起等
task(3)   # 1 秒
# 总共 3 秒
```

**问题**：等网络、等文件、等数据库的时候，Python 程序是**完全空转**的。

**异步**：等的时候把 CPU 让给别人，等单位重叠。

---

## 4 个关键词

| 词 | 意思 |
| --- | --- |
| `async def` | 定义一个**协程函数**（能中途让出去的函数） |
| `await` | **"我等着，但把时间让给别人"** |
| `asyncio.run(...)` | 启动"事件循环"，跑一个协程 |
| `asyncio.gather(*列表)` | 把多个协程**一起放出去**，全做完才返回 |

---

## 最小例子

```python
import asyncio

async def hello():
    await asyncio.sleep(1)      # 等 1 秒（但让出 CPU）
    return "好了"

结果 = asyncio.run(hello())
print(结果)                      # 好了
```

**注意三点**：

1. `async def` 定义的函数，**直接调用不会执行**，只是返回一个"协程对象"
2. 必须用 `asyncio.run(...)` 才会真正跑
3. `await` 只能写在 `async def` 里面

```python
async def f():
    return 1

f()              # <coroutine object f at 0x...>  ← 没跑！
asyncio.run(f()) # 1                              ← 这才跑
```

---

## 并发：`gather` 一次放多个

```python
import asyncio, time

async def task(n):
    await asyncio.sleep(1)
    return n * 2

async def main():
    任务列表 = []
    for i in range(3):
        任务列表.append(task(i))
    return await asyncio.gather(*任务列表)     # ← * 把列表拆成一个个参数

结果 = asyncio.run(main())
print(结果)      # [0, 2, 4]
# 耗时 1 秒，不是 3 秒
```

### `*任务列表` 是什么

```python
asyncio.gather(*任务列表)
# 等价于
asyncio.gather(任务1, 任务2, 任务3)
```

**`*` = 把列表"拆开"当成一个个参数传进去。** 这个符号在函数传参里叫"解包"。

---

## `await` 是全部的关键

```python
# ✅ 异步（让出去）
async def good():
    await asyncio.sleep(1)

# ❌ 假异步（照样卡住）
async def bad():
    time.sleep(1)        # 没用 await，整个程序还是卡 1 秒
```

**在 `async` 函数里用 `time.sleep()` = 白写异步。**

要等时间用 `asyncio.sleep()`，要发请求用支持异步的库（`httpx.AsyncClient`），要读文件用 `aiofiles`。

---

## 什么时候用，什么时候别用

| 场景 | 用异步？ | 为什么 |
| --- | --- | --- |
| 调 API（网络 IO） | ✅ **非常适合** | 等网络时能让出 CPU |
| 读大量文件 | ✅ 适合 | 等磁盘 |
| 数据库查询 | ✅ 适合 | 等数据库 |
| **算 100 万次乘法** | ❌ **没用，还更慢** | CPU 一直在忙，没得让 |
| 处理图片 / 视频编码 | ❌ 没用 | CPU 密集 |

### 为什么 CPU 密集不能用异步

**异步是"一个人同时干几件事"，前提是每件事都要"等"。**

如果每件事都在占着 CPU 算，那"同时干"就变成了"轮流干"——**还要额外花时间切换，反而更慢**。

> CPU 密集想并行 → 用 **多进程**（`multiprocessing`）。
> IO 密集想并行 → 用 **异步** 或 **多线程**。

---

## 常见坑

### 坑 1：忘了 `asyncio.run`

```python
async def f():
    return 1

f()          # ❌ 什么都没发生，也没有输出
asyncio.run(f())   # ✅
```

### 坑 2：在 `async def` 里用了同步函数

```python
async def bad():
    requests.get("https://...")     # ❌ requests 是同步的，整个程序卡住
    await httpx.get("https://...")  # ✅ 用支持异步的库
```

### 坑 3：`await` 写在普通函数里

```python
def f():
    await asyncio.sleep(1)    # ❌ SyntaxError: 'await' outside async function
```

**`await` 只能在 `async def` 里。**

### 坑 4：`asyncio.run` 嵌套调用

```python
async def a():
    asyncio.run(b())     # ❌ RuntimeError: asyncio.run() cannot be called from a running event loop
```

**一个程序只能有一个 `asyncio.run()`，在最外层。**

---

## 在项目里怎么用

### ① FastAPI 天然支持

```python
import asyncio

@app.post("/ask")
async def ask(req: AskRequest):        # ← 加 async 即可
    a = await 某异步函数(req.question)
    return {"answer": a}
```

FastAPI 会自动处理，你不用写 `asyncio.run`。

### ② 并发调多个模型做对比

```python
async def ask_model(model_name, question):
    await asyncio.sleep(0)             # 假装在调 API
    return f"{model_name} 的回答"

async def compare(question):
    tasks = []
    tasks.append(ask_model("deepseek", question))
    tasks.append(ask_model("其他模型", question))
    return await asyncio.gather(*tasks)     # 两个同时跑
```

### ③ 批量向量化

```python
# 1000 条笔记要 embed
# 同步：一条条等 → 慢
# 异步 + 并发 → 快很多（前提是用的库支持异步）
```

---

## 和其他并发方式的对比

| 方式 | 适合 | 一句话 |
| --- | --- | --- |
| **多线程** `threading` | IO 密集，但有 GIL 限制 | 一人多个线程，但要加锁 |
| **多进程** `multiprocessing` | **CPU 密集** | 开多个进程，真并行 |
| **异步** `asyncio` | **IO 密集（推荐）** | 一个人同时等多件事，不用锁 |

> **GIL**：CPython 里同一时刻只有一个线程能执行 Python 字节码，所以多线程不能让纯计算变快。异步不受这个限制。

---

## 速记卡

```
async def f():          定义一个协程
    await xxx()         await = 等着 + 让出 CPU
asyncio.run(f())        启动（最外层只写一次）
asyncio.gather(*列表)    并发跑多个

铁律：
  1. async 函数里必须用 await 的异步版本函数
  2. await 只能写在 async def 里
  3. CPU 密集别用异步，用多进程
```

---

## 🔗 相关

- 线程与进程：[17-线程与进程](17-线程与进程.md)（GIL / Lock / Condition）
- 语法体能：[03_语法体能3.py](../../../agent-lab/03-语法训练/03_语法体能3.py) 第 10 关
- 演示：[异步演示.py](../../../agent-lab/03-语法训练/异步演示.py)（3 秒 → 1 秒）
