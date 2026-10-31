---
title: LangChain 基础关键词（L1~L10）
category: LangChain
keywords: [LangChain, invoke, SystemMessage, HumanMessage, ChatPromptTemplate, StrOutputParser, tool, bind_tools, tool_calls, ToolMessage, tool_call_id, StateGraph, State, add_node, add_edge, compile, add_conditional_edges, ToolNode, add_messages]
dates: [2026-10-31]
---

# LangChain 基础关键词（L1~L10）

> 2026-10-31 从零重学 LangChain，10 课，每课只引入 1~2 个新词。
> 本文按课次列出**关键词 + 用法 + 一句话解释**，背下来就够用。

---

## L1 · 调用模型

| 词 | 用法 | 说明 |
| --- | --- | --- |
| `get_llm()` | `llm = get_llm()` | 我们自己写在 `config.py` 的工具：读 `.env` 的 key → 造出模型对象 |
| `.invoke(文本)` | `r = llm.invoke("你好")` | 问模型一次，**等**结果 |
| `.content` | `r.content` | 回答里的**文字** |
| `AIMessage` | `type(r).__name__` | 返回的不是字符串，是**消息对象**，文字必须用 `.content` 取 |

```python
llm = get_llm()
r = llm.invoke("用一句话介绍 Python")
print(r.content)
```

**关键**：`invoke` 返回消息对象，不是字符串。

---

## L2 · 定规矩（消息列表）

| 词 | 用法 | 说明 |
| --- | --- | --- |
| `SystemMessage("...")` | 放在列表第一条 | **定规矩**：身份、语气、格式 |
| `HumanMessage("...")` | 放在列表后面 | **你实际问的话** |

```python
messages = [
    SystemMessage("你是一个只说三个字的机器人"),
    HumanMessage("今天天气怎么样"),
]
r = llm.invoke(messages)      # 注意：传的是列表
```

**关键**：`SystemMessage` 决定回答风格，同一个问题换个 system 就换个性格。

---

## L3 · 提示词模板（带变量）

| 词 | 用法 | 说明 |
| --- | --- | --- |
| `ChatPromptTemplate` | `ChatPromptTemplate.from_messages([...])` | 提示词模板类 |
| `.from_messages([...])` | 里面是 `("system", "...")` 元组 | 用消息列表组装模板 |
| `{变量名}` | `"你是一个{role}"` | 占位符 |
| `prompt.invoke({...})` | `prompt.invoke({"role": "老师", "question": "你好"})` | **填空 → 得到消息列表** |

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}"),
    ("human", "{question}"),
])
messages = prompt.invoke({"role": "只说三个字的机器人", "question": "今天天气怎么样"})
r = llm.invoke(messages)
```

**关键**：模板**不回答**，它只负责生成消息列表（和你 L2 手写的一模一样）。

---

## L4 · 管道与输出解析

| 词 | 用法 | 说明 |
| --- | --- | --- |
| `\|`（管道） | `prompt \| llm` | 左边跑完的结果 → 交给右边 |
| `StrOutputParser()` | `prompt \| llm \| StrOutputParser()` | 把**消息对象**变成**纯文本**（省掉 `.content`） |

```python
chain = prompt | get_llm() | StrOutputParser()
answer = chain.invoke({"role": "诗人", "question": "写一句诗"})   # 直接是字符串
```

**关键**：`|` 在这里是"喂给下一步"，不是你以前学的集合并集。

---

## L5 · 工具（模型会"申请"）

| 词 | 用法 | 说明 |
| --- | --- | --- |
| `@tool` | `@tool` + 类型注解 + docstring | 把普通函数变成**工具对象**（`StructuredTool`） |
| `.bind_tools([...])` | `llm = get_llm().bind_tools([add])` | 告诉模型"你有这些工具"（**不执行**） |
| `.tool_calls` | `r.tool_calls` | 模型交的**申请单**（列表，每条是字典） |

`@tool` 之后函数身上的三样东西（都来自你的代码）：

| 属性 | 来自 |
| --- | --- |
| `.name` | 函数名 |
| `.description` | **docstring** |
| `.args` | **类型注解**（`a: int` → `{'type': 'integer'}`） |

```python
@tool
def add(a: int, b: int) -> int:
    """计算两个整数之和。"""
    return a + b

llm = get_llm().bind_tools([add])
r = llm.invoke("帮我算 123 + 456")
print(r.content)      # '' ← 空的，它没回答
print(r.tool_calls)   # [{'name': 'add', 'args': {'a': 123, 'b': 456}, 'id': 'call_00_xxx', 'type': 'tool_call'}]
```

**关键 1**：加 `@tool` 后 `add(1,2)` **报错**（`'StructuredTool' object is not callable`），要改成 `add.invoke({"a": 1, "b": 2})`。

**关键 2**：`tool_calls` 是**列表套字典**：

```
r.tool_calls                    → list   [ {...} ]          可能有多张申请单
r.tool_calls[0]                 → dict   {'name','args','id','type'}
r.tool_calls[0]["args"]         → dict   {'a': 123, 'b': 456}
r.tool_calls[0]["args"]["a"]    → int    123
```

> 同样是方括号：**列表里放数字**（取第几个），**字典里放字符串**（取哪个键）。

---

## L6 · 工具执行（手写闭环四步）

| 词 | 用法 | 说明 |
| --- | --- | --- |
| 工具 `.invoke({...})` | `mul.invoke(call["args"])` | 执行工具，参数用字典传 |
| `ToolMessage(...)` | `ToolMessage(content=str(结果), tool_call_id=call["id"])` | 把工具结果包装成**一条消息** |
| `tool_call_id` | `call["id"]` | **配对**：这个结果是哪张申请单的 |

```python
question = HumanMessage("计算 100 * 100")
r = llm.invoke([question])                       # ① 模型交申请单
call = r.tool_calls[0]
result = mul.invoke(call["args"])                # ② 你执行 → 10000
msgs = [question, r, ToolMessage(content=str(result), tool_call_id=call["id"])]
final = llm.invoke(msgs)                         # ③ 发回去 → 最终回答
```

**关键**：

- **模型只"说"不"做"**。它在 DeepSeek 服务器上，看不到你的时钟/硬盘，也没有执行函数的能力。
- 三种消息身份：`HumanMessage`（人说的）/ `AIMessage`（模型说的）/ `ToolMessage`（工具结果）。
- `ToolMessage.content` **只接受字符串**，所以 `str(result)`。
- `ToolMessage` 在 LangChain 源码里就是：

```python
class ToolMessage(BaseMessage):
    content: str
    tool_call_id: str
```

**为什么不用"再问一次"代替**：直接把结果拼进问题，模型不知道它是哪张申请单的结果；一次申请多个工具就全乱了。

---

## L7 · 最小的图（StateGraph）

| 词 | 用法 | 说明 |
| --- | --- | --- |
| `StateGraph(State)` | `g = StateGraph(State)` | 建图，图纸是 `State` |
| `State` | `class State(TypedDict): text: str` | 图里流动的数据长什么样 |
| `.add_node("名字", 函数)` | `g.add_node("a", step_a)` | 加节点 |
| `.add_edge(A, B)` | `g.add_edge("a", "b")` | 加边：A 之后走 B |
| `.compile()` | `app = g.compile()` | 编译（不编译不能跑） |
| `START` / `END` | `g.add_edge(START, "a")` | 起点 / 终点 |
| `.invoke({...})` | `app.invoke({"text": "开始"})` | 跑一次 |

```python
class State(TypedDict):
    text: str

def step_a(state: State) -> dict:
    return {"text": state["text"] + " → A"}      # 只返回【要改的字段】

g = StateGraph(State)
g.add_node("a", step_a)
g.add_edge(START, "a")
g.add_edge("a", END)
app = g.compile()
print(app.invoke({"text": "开始"}))      # {'text': '开始 → A'}
```

**关键**：节点**只返回要更新的字段**（不是整个 state），LangGraph 帮你合并。

---

## L8 · 图里塞模型

**0 个新词**——就是把 L1 的 `llm.invoke` 放进节点里。

```python
class State(TypedDict):
    question: str
    answer: str

def call_model(state: State) -> dict:
    r = llm.invoke(state["question"])
    return {"answer": r.content}
```

**关键**：模型只是节点里的一次函数调用；图负责"顺序、分支、循环"。

---

## L9 · 条件边（分支）

| 词 | 用法 | 说明 |
| --- | --- | --- |
| `.add_conditional_edges(起点, 判断函数, 映射表)` | `g.add_conditional_edges(START, decide, {"answer": "answer", "ignore": "ignore"})` | 岔路口 |
| 判断函数 | `def decide(state) -> str: return "节点名"` | **只返回字符串**，不改数据 |

```python
def decide(state: State) -> str:
    if "?" in state["text"]:
        return "answer"
    return "ignore"

g.add_conditional_edges(START, decide, {"answer": "answer", "ignore": "ignore"})
```

**关键**：分支能**省钱**——不是所有输入都值得调模型。走 `ignore` 分支的就完全不花 token。

---

## L10 · 工具接进图（L6 的自动版）

| 词 | 用法 | 说明 |
| --- | --- | --- |
| `ToolNode([工具])` | `g.add_node("tools", ToolNode(TOOLS))` | **现成的节点**，自动执行工具（替你干 L6 的 ②③ 步） |
| `add_messages` | `messages: Annotated[list, add_messages]` | 消息列表**自动追加**，不覆盖 |
| 循环 | `g.add_edge("tools", "agent")` | 工具执行完**回到 agent**（替你干 L6 的 ④ 步） |

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]     # ← 必须加 add_messages

def agent(state: State) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}

def should_continue(state: State) -> str:
    if getattr(state["messages"][-1], "tool_calls", None):
        return "tools"
    return END

g = StateGraph(State)
g.add_node("agent", agent)
g.add_node("tools", ToolNode(TOOLS))
g.add_edge(START, "agent")
g.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
g.add_edge("tools", "agent")            # ← 循环
app = g.compile()
```

**关键 1**：State 里不写 `add_messages`，第二轮消息会**覆盖**整个列表 → 工具结果丢失 → 死循环。

**关键 2**：`ToolNode` + 一条回边 = L6 手写的 12 行。跑出来的 4 条消息**一模一样**。

**关键 3**：模型可以**一次申请多个工具**（并行），ToolNode 全部执行，因此 L6 手写版只能调一次，图版能自动处理多个。

---

## 底层补充：原始 API 长什么样

绕过 LangChain，直接用 `openai` 库调 DeepSeek，返回的是：

```
ChatCompletionMessageFunctionToolCall(
    id='call_00_...',
    function=Function(arguments='{"a": 123, "b": 456}', name='add'),
    type='function',
)
```

| | 原始 API | LangChain |
| --- | --- | --- |
| 参数 | `arguments` = **JSON 字符串** | `["args"]` = **字典** |
| 工具名 | `.function.name` | `["name"]` |

**LangChain 的价值**：把各家模型五花八门的返回格式，统一成好用的 Python 对象（顺手把 JSON 字符串解析成字典）。

---

## 一句话总结（Agent 的心跳）

```
HumanMessage → AIMessage(申请单) → 你的代码执行 → ToolMessage → AIMessage(最终回答)
```

**这四步就是一个 Agent。** 所有框架（LangGraph、AutoGen…）底层都是这四步。

---

## 🔗 相关

- 课表：[LangChain 从零课表](../../plans/2026-10-31-LangChain从零课表.md)
- 当日记录：[2026-10-31](../../daily/2026-10-31.md)
- 代码：`agent-lab/L01.py` ~ `L10.py`
