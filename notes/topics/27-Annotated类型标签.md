---
title: Annotated（类型标签）
category: 进阶
keywords: [Annotated, typing, 类型元数据, get_type_hints, reducer, add_messages]
dates: [2026-10-26]
---

# Annotated（给类型贴标签）

> 一句话：`Annotated[类型, 标签]` = 给一个类型**额外附一条说明**，**运行时不改变任何行为**。
> 它是读懂 LangGraph `State` 的钥匙。

## 1. 是什么

普通类型注解只说明"这是什么类型"；`Annotated` 还能**额外挂一条元数据**（标签）。

```python
from typing import Annotated

# 普通注解
age: int

# 带标签的注解
age: Annotated[int, "用户年龄，单位岁"]
```

**关键**：那个标签**不影响运行**。`Annotated[int, "..."]` 在运行时就是 `int`。

## 2. 语法

```python
from typing import Annotated, get_type_hints

# 可以起个别名，方便复用
UserText = Annotated[str, "用户输入的文本"]


def read(text: UserText) -> str:
    return text


print(read("你好"))          # 你好（运行和普通 str 没区别）
```

## 3. 怎么把标签读出来

```python
hints = get_type_hints(read, include_extras=True)
print(hints)                      # {'text': Annotated[str, '用户输入的文本'], 'return': <class 'str'>}
print(hints["text"].__metadata__) # ('用户输入的文本',)
```

| 参数 | 作用 |
| --- | --- |
| `include_extras=True` | **必须加**，否则标签会被剥掉，只剩基础类型 |
| `.__metadata__` | 取出标签，是**元组** |

## 4. 标签可以是一个"函数"（重点）

```python
def merge(left, right):
    return left + right


Messages = Annotated[list, merge]     # 标签是 merge 这个函数
```

这就是 LangGraph 里那一行的真相：

```python
messages: Annotated[list[AnyMessage], add_messages]
#         └─ 类型：消息列表 ─┘  └─ 标签：合并方式 ─┘
```

翻译成人话：

> "`messages` 这个字段是列表；**有新数据来时，用 `add_messages` 的方式合并**（追加），不要整个覆盖。"

**注意**：这个位置**没有括号**（不是 `add_messages()`）。它不是在这里被调用，只是被"贴上去当说明"。真正调用它的是 **LangGraph 内部**。

## 5. 这个"标签函数"叫什么：reducer（归约器）

| 写法 | 新数据来时 |
| --- | --- |
| `messages: list` | **覆盖**（历史全丢） |
| `messages: Annotated[list, add_messages]` | **追加**（保留历史） |

> 这就是 Agent 能"记得上一轮工具结果"的原因。
> 少了 `Annotated[..., add_messages]`，就算加了 `checkpointer` 也会失忆。

## 6. Annotated / 普通注解 / dataclass / TypedDict 的关系

| 写法 | 作用 | 运行时 |
| --- | --- | --- |
| `x: int` | 只说类型 | 不校验 |
| `x: Annotated[int, "说明"]` | 类型 + 标签 | 不校验，标签可被读取 |
| `@dataclass` | 生成真正的类（有 `__init__`） | 会执行 |
| `class X(TypedDict)` | 声明字典的键 | 就是个普通 dict |

> 四者的共同点：**都用"类型注解"描述结构**。区别在于"运行时管不管"。

## 7. 自定义 reducer（进阶）

```python
def keep_last(left, right):
    """只保留最新的那条。"""
    return right


class State(TypedDict):
    latest: Annotated[str, keep_last]
```

LangGraph 每次更新 `latest` 时，会用 `keep_last(旧值, 新值)` 算出结果。

## ⚠️ 易错点速记

1. **`Annotated` 不改变运行行为**——它只是标签，别指望它做校验
2. 读标签必须 `include_extras=True`，否则标签丢了
3. `.__metadata__` 是**元组**，取第一个用 `[0]`
4. LangGraph 里 `add_messages` **是标签不是调用**——写 `add_messages` 不加括号
5. 忘了 `Annotated[..., add_messages]` → 消息被覆盖 → Agent 失忆
6. `Annotated` 从 `typing` 导入（Python 3.9+）

## 🔗 关联

- 类型注解基础 → [20-类型注解](20-类型注解.md)
- dataclass → [23-dataclass](23-dataclass.md)
- LangGraph 用法 → [26-LangGraph基础](26-LangGraph基础.md)
- 关键词表 → `agent-lab/basics/关键词表.md`
