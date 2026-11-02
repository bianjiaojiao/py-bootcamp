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

## L11 · 记忆（让它记住上一轮）

| 词 | 用法 | 说明 |
| --- | --- | --- |
| `checkpointer` | `g.compile(checkpointer=MemorySaver())` | **存档器**：每跑一步把对话存起来 |
| `MemorySaver()` | 存**内存**里的存档器 | 程序一退出就没了 |
| `thread_id` | `{"configurable": {"thread_id": "user-1"}}` | **会话编号**：同一个 id 共享记忆 |

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]     # ① 必须 add_messages

app = g.compile(checkpointer=MemorySaver())     # ② 必须传 checkpointer

config = {"configurable": {"thread_id": "user-1"}}    # ③ 必须带 thread_id
app.invoke({"messages": [HumanMessage("我叫小明")]}, config)
r = app.invoke({"messages": [HumanMessage("我叫什么？")]}, config)   # 记得
```

**记忆三件套，缺一不可**：

| # | 写在哪 | 作用 |
| --- | --- | --- |
| ① | `Annotated[list, add_messages]` | 消息**追加**（不覆盖） |
| ② | `compile(checkpointer=...)` | 每步**存档** |
| ③ | `invoke(..., {"configurable": {"thread_id": ...}})` | 存到**哪个编号**下 |

**怎么验证记忆真的生效**（实战技巧）：

```python
r["messages"][-1].response_metadata["token_usage"]["prompt_tokens"]
```

**第二轮的 `prompt_tokens` 明显大于第一轮 = 历史真的被送进去了。**

> 实测：第一轮 9 tokens → 第二轮 58 tokens → 换 thread_id 又回到 8 tokens。

---

## L12 · 人工确认（危险操作前暂停）

| 词 | 用法 | 说明 |
| --- | --- | --- |
| `interrupt("问题")` | **写在节点里** | 暂停整张图，把问题抛给人 |
| `Command(resume="回答")` | `app.invoke(Command(resume="yes"), config)` | 带着人的回答**恢复**执行 |
| `__interrupt__` | `r["__interrupt__"]` | 暂停时结果里多出的键，装着问题 |

```python
def risky(state):
    answer = interrupt("确认删除 3 个文件？(yes/no)")
    if answer == "yes":
        return {"approved": True, "messages": [("ai", "✅ 已删除")]}
    return {"approved": False, "messages": [("ai", "❌ 已取消")]}
```

**三步流程**：

```
① 第一次 invoke  → 跑到 interrupt 暂停，返回 __interrupt__
② 人看到问题     → 决定 yes / no
③ 第二次 invoke  → Command(resume="yes")，从暂停处继续
```

**关键点**：

| 要点 | 说明 |
| --- | --- |
| **必须 `checkpointer`** | 暂停后要存住状态，否则恢复不了 |
| **`interrupt()` 的返回值** | 就是人给的那个回答 |
| **可以写在节点中间** | 前面的代码执行完才停，**危险操作要放在它后面** |
| **一次暂停 = 两次 invoke** | 第一次暂停，第二次恢复 |

**这就是"你只做 yes/no"的形态**——平时 Agent 自己跑，只有要动真东西（删文件、发消息、付钱）时才问你。

---

## L13 · 流式输出

| 词 | 用法 | 说明 |
| --- | --- | --- |
| `.stream(...)` | `for chunk in llm.stream("问题"):` | 和 `invoke` 一样调用，但**逐片返回** |
| `chunk` | `chunk.content` | 每一小片的文字 |

```python
for chunk in llm.stream("用 50 个字介绍 Python"):
    print(chunk.content, end="", flush=True)
```

**两个容易漏的参数**：

| 参数 | 漏了会怎样 |
| --- | --- |
| `end=""` | 每片占一行，很难看 |
| `flush=True` | 攒在缓冲区，看不到"打字"效果 |

**`llm.stream` 和 `chain.stream` 的差别**：

| 写法 | 每片是什么 |
| --- | --- |
| `llm.stream("...")` | **消息对象** → 要用 `chunk.content` |
| `chain.stream({...})` | **字符串**（末尾有 `StrOutputParser`）→ 直接 `print(chunk)` |

**真正的价值不是总耗时**，而是**第一个字出现的时间**：`invoke` 要等 2 秒，`stream` 0.2 秒就开始冒字——用户感知完全不同（ChatGPT 那种界面就是这么做的）。

---

## 附：考核中暴露的 3 个共性弱点

> 2026-11-01 完成 10 题考核（4 题满分 / 5 题小修 / 1 题重做）。

| 弱点 | 具体表现 | 怎么改 |
| --- | --- | --- |
| **写完不跑，或只跑一半** | 只测 `if` 的一个分支；`TOOL = []` 一跑就发现 | 每写完一题**先跑一遍**再看代码 |
| **空实现忘了填** | 工具函数写了 `pass`；工具列表是空的 | 检查"我声明的每个东西都真的用上了吗" |
| **方法名凭印象写** | `text.reserve()`（字符串没有这个方法） | 字符串反转用 `text[::-1]`（专题 02 学过） |

---

## 🔗 相关

- 课表：[LangChain 从零课表](../plans/2026-10-31-LangChain从零课表.md)
- 当日记录：[2026-10-31](../daily/2026-10-31.md)、[2026-11-02](../daily/2026-11-02.md)
- 考核题目：[LangChain考核-10题](../../LangChain考核-10题.md)
- 代码：`agent-lab/L01.py` ~ `L13.py`，考核答案 `exercises/作业111/langchain-kaohe/`
