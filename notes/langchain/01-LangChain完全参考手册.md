---
title: LangChain / LangGraph 完全参考手册
category: 工程
keywords: [LangChain, LangGraph, 参考手册, 关键词, 模板, 调用方式]
dates: [2026-10-27]
---

> 本文件是归档版。工作副本在 `agent-lab/basics/LangChain完全参考手册.md`（两处内容相同）。

# LangChain / LangGraph 完全参考手册

> **怎么用**：这是"查词典 + 抄模板"用的，不是从头读的。写代码时遇到不认识的词→查第 3 节；要写某类功能→抄第 5 节的模板改。
> **别背**：查十遍自然记住。

---

## 1. 两张全景图（一切代码都是它的变体）

### LangChain = 一条流水线

```
提示词模板 ──► 模型 ──► 消息 ──► 解析器 ──► 纯文本
                   ▲
                工具（模型只"请求"调用，不执行）
```

### LangGraph = 一张图

```
状态(State) ──► 节点(Node) ──► 边(Edge) ──► 编译(compile) ──► 调用(invoke)
                    ▲                            │
                    └────── 循环可能回到这里 ─────┘
```

**读任何 LangChain/LangGraph 代码，先问：这是流水线的哪一段？这是图的哪部分？**

---

## 2. Python 语法模式（LangChain 代码 90% 的行）

### 2.1 五种代码模板

| # | 模板 | 例子 | 意思 |
|---|---|---|---|
| ① | `名字 = 类(参数)` | `llm = ChatOpenAI(...)`、`g = StateGraph(State)` | **创建**对象 |
| ② | `对象.方法(参数)` | `llm.invoke(...)`、`g.add_node(...)` | 让对象**做一件事** |
| ③ | `对象.方法().方法()` | `get_llm().bind_tools(TOOLS)` | 链式：前一步返回对象，紧接着再调用 |
| ④ | `对象 \| 对象` | `prompt \| llm \| parser` | **管道**：左边输出 → 右边输入 |
| ⑤ | `@装饰器` | `@tool` | 给函数**加工**（包装） |

### 2.2 import 规则

```python
from 包.模块 import 名字
```

= 把 `名字` **搬**进来。**import 不执行业务逻辑**，只是"拿零件"。

判断搬来的是什么：**类**（可 `X()` 创建）/**函数**（可 `f()` 调用）/**常量**（直接用，不能加括号）。

### 2.3 类 / 函数 / 常量怎么分

```python
StateGraph(State)      # StateGraph 是类 → 加括号 = 创建
get_llm()              # get_llm 是函数 → 加括号 = 调用
END, START             # 常量 → 直接写，加括号会报错
```

---

## 3. 关键词词典（按类别查）

### 3.1 模型

| 词 | 人话 | 用法 / 注意 |
|---|---|---|
| `ChatOpenAI` | 创建模型对象的类（DeepSeek 借它的通道） | `ChatOpenAI(model="deepseek-chat", api_key=..., base_url="https://api.deepseek.com")` |
| `llm` | 模型对象（约定俗成的变量名） | 我们的 `config.get_llm()` 帮你配好 key/url |
| `.invoke(输入)` | **同步调用一次，等结果** | `llm.invoke("你好")` 返回消息对象 |
| `.batch([a, b])` | 批量调用多个输入 | 一次发一批，返回列表 |
| `.stream(输入)` | 流式：一个个字往外吐 | `for chunk in llm.stream(...)` |
| `temperature` | 随机性。0 最稳，1 最大胆 | 抽结构化/算数用 0；写文案用 0.7+ |
| `max_tokens` | 回答最长多少 token | 控成本用 |
| `.bind_tools([...])` | 把工具清单"装备"给模型 | 返回的仍是模型对象（可继续 .invoke） |
| `.with_structured_output(类, method=...)` | 让回复直接变成对象 | DeepSeek 必须 `method="function_calling"` |

### 3.2 消息

| 词 | 人话 | 注意 |
|---|---|---|
| `HumanMessage` | 用户说的话 | `HumanMessage(content="你好")` |
| `AIMessage` | 模型说的话 | 用 `.content` 取文字 |
| `SystemMessage` | 系统设定（人设） | 用 `.content` 取文字 |
| `ToolMessage` | 工具执行的结果 | 有 `tool_call_id`，与请求配对 |
| `AnyMessage` | 以上任意一种（类型注解用） | 只出现在类型注解里 |
| `.content` | 消息里的**文字** | 模型返回的不是字符串！ |
| `.tool_calls` | 模型发的"调用请求"列表 | `[{'name':'add','args':{'a':1,'b':2},'id':...}]` |
| `tool_call_id` | 每次工具请求的编号 | `ToolMessage` 必须带它配对 |
| `.usage_metadata` | token 用量 | 算成本、评估用 |
| `messages` | 消息列表 = 对话历史 | 图里流动的核心数据 |

### 3.3 提示词

| 词 | 人话 | 用法 |
|---|---|---|
| `ChatPromptTemplate` | 带变量的提示词模板 | 见 5.2 |
| `.from_messages([...])` | 用消息列表组装模板 | 列表元素是 `("角色", "内容")` 元组 |
| `.from_template("...")` | 从一段带变量的文本建模板 | 简单场景用 |
| `("system", "…")` | 一条系统消息 | 定人设/规则 |
| `("human", "{q}")` | 一条用户消息 | `{q}` 是待填变量 |
| `MessagesPlaceholder("history")` | 插历史消息的位置 | 多轮对话用 |
| `{变量}` | 占位符 | 调用时用字典填值 |
| `.partial(变量=值)` | 提前固定部分变量 | 少传参用 |

### 3.4 链 / 输出

| 词 | 人话 | 注意 |
|---|---|---|
| `chain` | 一条拼好的流水线 | `prompt \| llm \| parser` |
| `\|` | 管道符：**左边输出 → 右边输入** | LangChain 重载了这个运算符 |
| `LCEL` | 用 `\|` 拼链的那套写法 | LangChain Expression Language |
| `StrOutputParser()` | 消息对象 → 纯文本 | 新版返回 `TextAccessor`（str 子类） |
| `JsonOutputParser()` | 消息文本 → dict | 需在提示词里要求输出 JSON |
| `RunnablePassthrough()` | 原样传递 | `{"问题": 原样, "摘要": 链}` |
| `RunnableLambda(函数)` | 把普通函数接进链 | `RunnableLambda(process)` |
| `RunnableParallel(...)` | 并行跑多个分支 | 见 5.11 |

### 3.5 结构化输出

| 词 | 人话 | 注意 |
|---|---|---|
| `BaseModel` | Pydantic 的"结构图纸"类 | `class Movie(BaseModel)` |
| `Field(description="…")` | 给字段写**给模型看的说明** | 说明越清楚，抽取越准 |
| `.with_structured_output(Movie, method="function_calling")` | 让输出变成 Movie 对象 | **DeepSeek 必须 function_calling** |
| `method="json_schema"` | 默认方式 | ❌ DeepSeek 不支持 |
| `method="json_mode"` | 返回 JSON 文本 | ✅ 但要自己提示 + 解析 |

### 3.6 工具

| 词 | 人话 | 注意 |
|---|---|---|
| `@tool` | 把普通函数包装成"工具" | 写在 `def` 上一行 |
| docstring | **给模型看的说明书** | 决定模型会不会选它，必须写清楚 |
| `args_schema` | 用 Pydantic 精确描述参数 | 类型注解不够用时加 |
| `bind_tools([...])` | 告诉模型"你有这些工具" | 装备后才可能产生 tool_calls |
| `tool_calls` | 模型发的调用请求 | 模型**不执行**，只是"请求" |
| `ToolNode(TOOLS)` | 图里负责**执行工具**的节点 | 它会真正调用 add(1,2) |
| `TOOLS` | 工具列表（普通 list） | `TOOLS = [add, search]` |
| `tool_choice` | 强制/禁止调用工具 | 进阶参数 |

### 3.7 图（LangGraph）

| 词 | 人话 | 注意 |
|---|---|---|
| `StateGraph(State)` | 用 State 图纸**创建**一张空图 | StateGraph 是**类** |
| `State` | 图里流动的"数据袋子" | 用 `TypedDict` 声明 |
| `TypedDict` | 声明"这个字典有哪些键" | 运行时仍是普通 dict，**不校验** |
| `Annotated[list, add_messages]` | "列表用**累加**方式更新" | `add_messages` 是标签**不是调用**（无括号） |
| `add_messages` | 累加函数（reducer） | 真正调用发生在图内部 |
| `add_node("名字", 函数)` | 加一个节点（工位） | 两个参数：字符串标签 + 函数对象 |
| `add_edge(A, B)` | 加固定连线 A→B | |
| `add_conditional_edges("A", 判断函数, {分支映射})` | 加岔路口 | 判断函数返回字符串，映射表决定去哪 |
| `.compile()` | 把图纸变成能跑的机器 | **不加 compile 图不能用** |
| `START` / `END` | 起点 / 终点常量 | 不能加括号 |
| `app.invoke({"messages": [...]})` | 跑一次图 | 输入是初始状态字典 |
| `recursion_limit` | 最大步数上限 | 死循环时靠它停下来 |
| `ToolNode(TOOLS)` | 现成的"执行工具"节点 | 从 `langgraph.prebuilt` 导入 |

### 3.8 记忆

| 词 | 人话 | 注意 |
|---|---|---|
| `MemorySaver()` | 存档器：状态存内存 | 程序重启就没了 |
| `SqliteSaver` | 存档器：存文件 | 可持久化（需额外装包） |
| `checkpointer` | 传给 `compile(checkpointer=...)` | 有了它图才"记得" |
| `thread_id` | 会话身份证 | 同一个 id = 同一段记忆 |
| `{"configurable": {"thread_id": "..."}}` | 调用时指明"用哪个会话" | 传给 invoke 的第二个参数 |
| `.get_state(config)` | 查看会话存了什么 | 空会话 `values` 是空 dict，用 `.get()` |
| `.update_state(config, ...)` | 手动改写状态 | 时间旅行用 |

### 3.9 人工介入 / 流式

| 词 | 人话 | 注意 |
|---|---|---|
| `interrupt(提示)` | 图跑到这里**暂停**，等人回应 | 从 `langgraph.types` 导入 |
| `Command(resume=值)` | 恢复执行并回传答案 | `app.invoke(Command(resume="yes"), config)` |
| `.stream(输入, stream_mode="updates")` | 流式看每一步 | `"updates"`=看节点更新；`"values"`=看全状态 |

### 3.10 报错与防护

| 词 | 人话 |
|---|---|
| `handle_parsing_errors` | 工具调用解析失败时自动重试 |
| `max_iterations` | Agent 最多转几圈 |
| `retry` | 网络失败重试（tenacity） |
| `recursion_limit` | 图的步数上限 |

---

## 4. 调用方式汇总

### 4.1 三种调用（模型 / 链 / 图都适用）

| 方式 | 干什么 | 返回 |
|---|---|---|
| `.invoke(x)` | 同步跑一次，等结果 | 最终结果 |
| `.batch([x1, x2])` | 一批输入一起跑 | 结果列表 |
| `.stream(x)` | 流式，边生成边吐 | 迭代器（for 循环取） |

### 4.2 传参的两种样子

```python
# 模型：直接传文本或消息列表
llm.invoke("你好")
llm.invoke([HumanMessage("你好")])

# 链：传字典（给 {变量} 填值）
chain.invoke({"question": "什么是闭包"})

# 图：传"初始状态"字典
app.invoke({"messages": [HumanMessage("...")]})
```

### 4.3 常见"返回值长什么样"

```python
r = llm.invoke("你好")
type(r)          # AIMessage
r.content        # 纯文本

c = chain.invoke({"question": "..."})
type(c)          # str（因为末尾有 StrOutputParser）

s = app.invoke({"messages": [...]})
type(s)          # dict，键就是 State 里声明的键
```

---

## 5. 常见模板（可直接抄，改标 ⭐ 处）

### 5.1 最简调用模型

```python
from config import get_llm

llm = get_llm(temperature=0)
r = llm.invoke("你好")          # ⭐ 换成你的问题
print(r.content)
```

### 5.2 提示词 + 链 + 输出解析

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import get_llm

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位耐心的 Python 老师"),   # ⭐ 人设
        ("human", "{question}"),
    ]
)
chain = prompt | get_llm() | StrOutputParser()
answer = chain.invoke({"question": "什么是闭包？"})   # ⭐ 问题
print(answer)
```

### 5.3 工具定义 + 绑定

```python
from langchain_core.tools import tool
from config import get_llm

@tool
def add(a: int, b: int) -> int:
    """计算两个整数之和。"""      # ⭐ 说明书（模型靠它决定用不用）
    return a + b

llm = get_llm(temperature=0).bind_tools([add])
r = llm.invoke("帮我算 1 + 2")
print(r.tool_calls)              # 模型只发请求，不执行！
```

### 5.4 结构化输出（DeepSeek 版）

```python
from pydantic import BaseModel, Field
from config import get_llm

class Movie(BaseModel):
    title: str = Field(description="片名")     # ⭐ 字段与说明
    year: int = Field(description="上映年份")

structured = get_llm(temperature=0).with_structured_output(
    Movie, method="function_calling"           # ⭐ DeepSeek 必须这一行
)
movie = structured.invoke("《流浪地球》是 2019 年的科幻片")
print(movie.title, movie.year)
```

### 5.5 最小图（无工具）

```python
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from config import get_llm

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def agent(state: State) -> dict:
    return {"messages": [get_llm().invoke(state["messages"])]}

g = StateGraph(State)
g.add_node("agent", agent)
g.add_edge(START, "agent")
g.add_edge("agent", END)
app = g.compile()

r = app.invoke({"messages": [HumanMessage(content="你好")]})  # ⭐ 问题
print(r["messages"][-1].content)
```

### 5.6 工具循环（完整 Agent 图）

```python
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
# （State / llm 同 5.5，llm 需 bind_tools）

@tool
def add(a: int, b: int) -> int:
    """计算两个整数之和。"""
    return a + b

TOOLS = [add]
llm = get_llm(temperature=0).bind_tools(TOOLS)

def agent(state: State) -> dict:
    return {"messages": [llm.invoke(state["messages"])]}

def should_continue(state: State) -> str:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tools"
    return END

g = StateGraph(State)
g.add_node("agent", agent)
g.add_node("tools", ToolNode(TOOLS))
g.add_edge(START, "agent")
g.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
g.add_edge("tools", "agent")          # ← 循环的关键
app = g.compile()
```

### 5.7 带记忆（跨轮记住）

```python
from langgraph.checkpoint.memory import MemorySaver

app = g.compile(checkpointer=MemorySaver())      # ⭐ 就多这一个参数

config = {"configurable": {"thread_id": "user-1"}}   # ⭐ 会话身份证
app.invoke({"messages": [("user", "我叫小明")]}, config)
app.invoke({"messages": [("user", "我叫什么？")]}, config)   # 它记得！
```

> 注意：节点里的 `state["messages"]` 之所以有历史，靠的是
> `Annotated[..., add_messages]` + checkpointer **两个一起**。

### 5.8 人工确认（危险操作前暂停）

```python
from langgraph.types import Command, interrupt

def risky_node(state):
    answer = interrupt({"question": "要删除这个文件吗？(yes/no)"})  # ⭐ 暂停
    if answer != "yes":
        return {"messages": [("ai", "已取消")]}
    # 继续执行删除……
    return {"messages": [("ai", "已删除")]}

# 第一次跑：会停在这里，把 interrupt 的问题抛给你
# 恢复：app.invoke(Command(resume="yes"), config)   # ⭐ 你答 yes 后继续
```

### 5.9 流式输出

```python
# 模型级：一个字一个字出来
for chunk in llm.stream("写一首五言绝句"):
    print(chunk.content, end="", flush=True)

# 图级：看每一步发生了什么
for step in app.stream({"messages": [...]}, stream_mode="updates"):
    print(step)
```

### 5.10 RAG 最简链（概念版，embedding 待装）

```python
# 流程：读文档 → 切分 → 向量化 → 存向量库 → 检索 → 拼提示词 → 生成
# 依赖：langchain-text-splitters + 向量库 + embedding 模型（阶段 4 再装）

from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_text(长文档文本)
# chunks 存入向量库（Chroma/FAISS），检索出最相关的几段，
# 拼进 5.2 的提示词里当背景知识，再问模型。
```

### 5.11 并行分支（进阶）

```python
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

chain = {
    "原问题": RunnablePassthrough(),
    "语气": 提示链 | llm | StrOutputParser(),
}
# 输入一句话，同时产出"原样转发"和"改写语气"两路
```

---

## 6. 常见报错速查

| 报错 | 原因 | 解法 |
|---|---|---|
| `ModuleNotFoundError: No module named 'config'` | 脚本不在 agent-lab 根目录 | 文件头加 3 行 `sys.path.insert`（见你 01.py 开头） |
| `This response_format type is unavailable now` | DeepSeek 不支持 json_schema | `method="function_calling"` |
| `401 / AuthenticationError` | key 错/空格/没余额 | 检查 `.env` |
| `KeyError: 'messages'` | 查了从没跑过的线程 | `(state.values or {}).get("messages", [])` |
| `GraphRecursionError` | 死循环 | 检查条件边是否返回 END；调 `recursion_limit` |
| `ToolMessage 缺 tool_call_id` | 手动构造工具消息 | 用 `ToolNode` 自动处理 |
| 输出是 `content='...'` 那一坨 | 忘了加解析器 | 链末尾加 `StrOutputParser()` |
| 新消息把历史覆盖了 | State 字段少了 `Annotated[..., add_messages]` | 加上 |
| 多轮对话记不住 | 没传 checkpointer 或 thread_id | 两个都要 |

---

## 7. 读陌生代码的四步

1. **看 import**：有哪些零件？（类 / 函数 / 常量）
2. **找 class**：数据结构是什么样
3. **找 def**：节点函数有哪些，输入输出是什么
4. **从下往上读**：执行入口在最后几行
