# LangChain 从零课表（严格先教后练）

> 建立：2026-10-31
> **铁律**：
> 1. 每课**只引入 1~2 个新词**，逐个讲清"它是什么、干什么用"
> 2. 练习**只允许用本课新词 + 已确认学过的旧词**（下面有"已学清单"）
> 3. 出现没教过的词 = 我的错，你可以直接拒绝做
> 4. **一课一验收**：练习跑通、你能用自己的话解释，才进下一课

---

## 已学清单（只有这些算"学过"）

### A. Python 语言（已确认会，来自 28 篇专题 + drills）

| 类别 | 具体能力 |
| --- | --- |
| 基础 | 变量、`print`、f-string、切片、`len()`、`type(x).__name__` |
| 流程 | `if/elif/else`、`for/while`、`break/continue` |
| 容器 | 列表、元组、字典（含 `.get()`）、集合（含 `\|` 并集）、推导式 |
| 函数 | 默认参数、`*args/**kwargs`、多返回值+解包 |
| 进阶 | 闭包 + `nonlocal`、装饰器（五步骨架）、生成器 `yield`、`iter/next` |
| 面向对象 | 类、`__init__`、`self`、实例/类属性、继承、`isinstance`、`__eq__`/`__hash__` |
| 类型 | `dataclass`、`TypedDict`、`Annotated`、`getattr` |
| 其它 | `try/except`、`raise`、`pathlib`、`json`、`import` 语法、`Enum/IntEnum`、`type()` 建类、`__init_subclass__`、`threading`（Thread/Lock/Condition） |

### B. 环境与运行

| 项 | 说明 |
| --- | --- |
| `agent-lab` 环境 | 有 venv，用 `.venv\Scripts\python.exe 文件名.py` 跑，且要在 `agent-lab` 目录下 |
| `config.py` | 第 0 课专门讲：`load_dotenv` / `os.getenv` / `ChatOpenAI(4 参数)` |

### C. LangChain（每课学完加一行）

| 课 | 新词 | 状态 |
| --- | --- | --- |
| 0 | `ChatOpenAI` 4 参数（`pathlib` 读 `.env` 是复习，不算新词） | 🔄 进行中 |
| 0b | `load_dotenv()`、`os.getenv()` | ⬜ |
| 1 | — | ⬜ |

---

## ⚠️ 隐藏前提审计（每课的"坑"提前列出来）

> 这些不是新知识，但**不说就会卡住**。到时候我会在本课里明确提一句。

| 课 | 隐藏前提 | 处理 |
| --- | --- | --- |
| **0** | ① Windows 控制台 GBK → 中文乱码<br>② `load_dotenv()` 从**当前目录**找 `.env` | ✅ 已写进 `L00_示例.py` 注释和练习要求 |
| 1 | `get_llm()` 是封装（第 0 课刚拆过） | ✅ 已铺垫 |
| 2 | 消息列表 = 普通 Python 列表 | ✅ 已会 |
| 3 | `.invoke({...})` 传的是字典 | ✅ 已会 |
| **4** | **`\|` 对"对象"也能用**（运算符重载；你之前见的是集合的并集） | ⚠️ 到第 4 课明确讲 1 段 |
| 5 | `@tool` 就是装饰器；docstring 会被模型看到 | ✅ 装饰器已会 |
| 6 | `BaseModel` 和 `dataclass` 的区别 | ✅ 类比讲 1 段 |
| 7 | `State` 用 `TypedDict` 写 | ✅ 已会 |
| 8 | `Annotated` 已在专题 28 学过 | ✅ 已会 |
| 9~13 | 无额外前提（都是本课新词） | — |

---

## 15 课（每课 15~25 分钟）

| 课 | 只教这些新词 | 练习（只用到左边这些 + Python 基础） |
| --- | --- | --- |
| **0** | `ChatOpenAI` 的 4 个参数 | **用 pathlib 手读 `.env`** 取 key + 造模型对象（零其他新词） |
| **0b** | `load_dotenv()`、`os.getenv()` | 用两行替代你第 0 课手写的那 20 行（体会"封装"） |
| **1** | `llm`、`.invoke()`、`.content` | 问一句，打印回复 + 打印类型 |
| **2** | `HumanMessage`、`SystemMessage`、消息列表 | 用 system 改变回答风格 |
| **3** | `ChatPromptTemplate`、`from_messages`、`{变量}` | 做一个带变量的模板 |
| **4** | `\|`（管道）、`StrOutputParser` | 把三步串成一条链 |
| **5** | `@tool`、docstring、`bind_tools`、`.tool_calls` | 写一个工具，看模型"请求"调用 |
| **6** | `BaseModel`、`Field`、`with_structured_output` | 让回复变成一个对象 |
| **7** | `StateGraph`、`State`、`add_node`、`add_edge`、`compile` | 搭一个两节点图跑通 |
| **8** | `TypedDict`、`Annotated`、`add_messages` | 让图里能装对话历史 |
| **9** | `add_conditional_edges`、`END` | 给图加一个岔路口 |
| **10** | `ToolNode`、工具循环 | 把工具接进图 |
| **11** | `checkpointer`、`MemorySaver`、`thread_id` | 让它记住上一轮说过的话 |
| **12** | `interrupt`、`Command` | 危险操作前暂停等人确认 |
| **13** | `.stream()` | 逐字输出 |

---

## 每课固定结构

1. **概念**：这个新词是什么、解决什么问题（3~5 句，不用术语解释术语）
2. **示例**：我给一个 10 行以内的可运行文件，你**先跑一遍看结果**
3. **练习**：一个只用到本课新词的**空文件**，你从零写
4. **验收**：输出长什么样算通过

---

## `os` 模块要学多少（2026-10-31 实测）

**查了你两个项目里所有 `.py` 文件**（排除 `.venv`），`os` 的用法只有一种：

| 用法 | 出现次数 | 在哪 |
| --- | --- | --- |
| `os.getenv(...)` | **8 次** | 全部在 `agent-lab/config.py` 和 `course-rag/config.py` |
| 其它 `os.xxx` | **0 次** | — |

所以**现在只需要学 `os` 的一个函数**：

| 要学 | 说明 |
| --- | --- |
| `os.getenv("名字", "默认值")` | 从环境变量取值（第 0b 课） |
| `os.environ` | 全部环境变量的字典（顺便知道，同一课） |

**不用现在学的**——`pathlib` 已经覆盖了：

| 老的 os 写法 | 现在用 pathlib |
| --- | --- |
| `os.path.join(a, b)` | `Path(a) / b` |
| `os.listdir(".")` | `Path(".").iterdir()` |
| `os.makedirs(p, exist_ok=True)` | `Path(p).mkdir(parents=True, exist_ok=True)` |
| `os.getcwd()` | `Path.cwd()` |
| `os.path.exists(p)` | `Path(p).exists()` |

> 结论：**"学 os" ≠ 学整套 os**。你现在只需要 `os.getenv` 一个，其余用到再说。

---

## 课表之外的旧东西怎么办

之前 `agent-lab/` 里的 `01_hello_llm.py` ~ `99_langchain_速览.py`、`drills/`、`course-rag/` 都先**放着不动**。
等走到第 7~13 课，你会发现"原来那些文件就是这节课的内容"——那时候再回头看就不会懵了。

> **不要提前看那些文件**，它们混了多个知识点，现在看只会更乱。

---

## 代码风格铁律（2026-11-02 追加）

> 起因：示例代码里用了 `enumerate(QUESTIONS, 1)`、元组解包、`sorted(set(...))`、`{!r}`，
> 这些**跟当课知识点无关**，反而让人分心。

| 不许出现 | 除非 |
| --- | --- |
| `enumerate` / 元组解包 | 本课就是在讲它 |
| 列表推导式 / 生成器表达式 | 本课就是在讲它 |
| `sorted` / `set` / `functools` 等技巧 | 本课就是在讲它 |
| f-string 的格式说明符（`{x:>6.2f}`、`{!r}`） | 本课就是在讲它 |
| 一行写多个操作（`a = f(g(h(x)))`） | 拆成三行 |
| 复杂的 `for` + 条件嵌套 | 拆成平铺的几段 |

**执行标准**：

- 示例代码要**能一眼看完**，每行只干一件事
- 宁可写 3 遍重复的代码，也不为了"优雅"引入没教过的语法
- 只保留"本课新词 + 已确认学过的语法"
