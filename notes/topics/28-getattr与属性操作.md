---
title: getattr 与属性操作
category: 进阶
keywords: [getattr, hasattr, setattr, 属性, 反射, tool_calls, 安全取值]
dates: [2026-10-29]
---

# getattr 与属性操作

> 一句话：平时写 `obj.name` 是**写死**属性名；属性名**运行时才知道**时，要用 `getattr`。

## 1. 为什么需要它

```python
user = User()

print(user.name)          # ✅ 属性名写死在代码里
attr = "name"
print(user.attr)          # ❌ 这不是"取 attr 变量里的属性"，而是找名叫 attr 的属性
```

想用**变量里存的属性名**去取值，就必须用 `getattr`。

## 2. 三兄弟

| 函数 | 作用 | 等价于 |
| --- | --- | --- |
| `getattr(obj, "名字", 默认值)` | 取属性；**不存在时返回默认值而不报错** | `obj.名字`（但没有兜底） |
| `hasattr(obj, "名字")` | 判断有没有这个属性，返回 `True`/`False` | `try: obj.名字; True except: False` |
| `setattr(obj, "名字", 值)` | 设置属性 | `obj.名字 = 值` |

```python
class User:
    name = "小明"

u = User()
print(getattr(u, "name", "匿名"))    # 小明
print(getattr(u, "age", "未知"))     # 未知   ← 没有 age，返回默认值
print(hasattr(u, "age"))             # False

setattr(u, "age", 20)
print(u.age)                         # 20
```

## 3. 最常用的场景：Agent 代码里判断"模型想不想调工具"

```python
last = state["messages"][-1]

# 模型想调工具时，这条消息身上会多出 tool_calls 属性
if getattr(last, "tool_calls", None):
    return "tools"
return END
```

> **为什么不直接写 `last.tool_calls`？**
> 因为普通消息（比如用户消息、最终回答）**没有**这个属性，直接点会 `AttributeError`。
> 用 `getattr(..., None)` 就变成"有就取，没有就是 None"，永远不会崩。

## 4. 不给默认值的后果

```python
getattr(u, "age")        # ❌ AttributeError: 'User' object has no attribute 'age'
```

| 写法 | 属性不存在时 |
| --- | --- |
| `getattr(obj, "x")` | 抛 `AttributeError` |
| `getattr(obj, "x", None)` | 返回 `None` ✅ |
| `getattr(obj, "x", 默认值)` | 返回默认值 ✅ |

**口诀**：**不确定属性在不在，第三个参数一定要给。**

## 5. `hasattr` + `getattr` 配合的写法

```python
if hasattr(obj, "x"):
    value = getattr(obj, "x")
else:
    value = "默认"

# 等价于更简洁的一行：
value = getattr(obj, "x", "默认")
```

> 能用 `getattr` 的默认值解决，就别写 if/else。

## 6. 和字典 `.get()` 的对照（同一个套路）

| 数据类型 | 安全取值 | 硬取会怎样 |
| --- | --- | --- |
| 字典 | `d.get(k, 默认值)` | `d[k]` → `KeyError` |
| 对象属性 | `getattr(obj, k, 默认值)` | `obj.k` → `AttributeError` |

**这是同一个思想的两种形式**：**不确定存在时，用"带默认值的取值函数"。**

## ⚠️ 易错点速记

1. `getattr` 的第二个参数必须是**字符串**：`getattr(obj, "name")`，不能 `getattr(obj, name)`（那是变量）
2. 三个参数里，第三个是**默认值**，不是"类型"
3. `hasattr` 返回布尔值，取不到具体内容
4. 属性不存在且没给默认值 → `AttributeError`
5. `getattr` 也能取**方法**（`m = getattr(obj, "hello")` 之后 `m()` 就是调用）

## 🔗 关联

- 字典 `.get()`（同一个套路）→ [04-字典](04-字典.md)
- 特殊方法（`__eq__`/`__hash__` 等）→ [13-特殊方法与哈希](13-特殊方法与哈希.md)
- LangGraph 里用它判断 `tool_calls` → [26-LangGraph基础](26-LangGraph基础.md)
- 原始截图 → [source/2026-10-29/A.md](../source/2026-10-29/A.md)（图 image71）
