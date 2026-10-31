# Python 学习笔记 · 截图转写（2026-10-31 新增部分）

> 来源：`py-bootcamp/新建 DOC 文档.doc`（累积文档，本次共 **95** 张截图）。
> 前 88 张已在之前转写完成，本次新增 **7 张**（image89 ~ image95）。
>
> 主题：**LangChain L5~L7 的代码截图 + `ToolMessage` 底层定义**

---

## 图 image89 — `call = r.tool_calls[0]`

**第一行：`call = r.tool_calls[0]`**

**大白话翻译**："大模型可能一次性发了好几张申请单（比如既要算乘法，又要查天气），列表里有很多个。我只要第一张。"

- 执行后，`call` 变成了那个字典：`{'name': 'mul', 'args': {'a': 100, 'b': 100}, 'id': 'call_123'}`。

---

## 图 image90 — `result = mul.invoke(call["args"])`

**第二行：`result = mul.invoke(call["args"])`**

**大白话翻译**："从单子里抠出参数 `call["args"]`（也就是 `{'a': 100, 'b': 100}`），然后塞给 `mul` 函数去执行。"

- 这一步等价于你手写了：`result = mul(a=100, b=100)`。
- 函数算完，`result` 拿到了结果 `10000`。

---

## 图 image91 — `r = llm.invoke([question])`

```python
r = llm.invoke([question])
```

---

## 图 image92 — 取申请单 + 执行工具

```python
call = r.tool_calls[0]
result = mul.invoke(call["args"])
```

---

## 图 image93 — LangChain 底层 `ToolMessage` 定义

如果你去翻 LangChain 的底层源码，它的核心定义大概长这样：

```python
class ToolMessage(BaseMessage):
    content: str
    tool_call_id: str
```

它继承自基础消息类，但**强制要求必须传入两个核心参数**。

---

## 图 image94 — 三条消息 + 发回模型

```python
message = [
    question,
    r,
    ToolMessage(content=str(result), tool_call_id=call["id"])
]
a = llm.invoke(message)
print(a.content)
```

---

## 图 image95 — StateGraph 建图

```python
g = StateGraph(State)
g.add_node("a", add_a)
g.add_node("b", add_b)
g.add_edge(START, "a")
g.add_edge("a", "b")
g.add_edge("b", END)
app = g.compile()

result = app.invoke({"text": "开始"})
print(result)
```

---

## 涉及的专题

| 截图 | 对应专题 |
| --- | --- |
| image89 ~ image94 | [29-LangChain基础关键词](../../topics/29-LangChain基础关键词.md)（L5~L6 部分） |
| image95 | [29-LangChain基础关键词](../../topics/29-LangChain基础关键词.md)（L7 部分） |
