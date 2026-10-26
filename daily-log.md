# 学习日志（daily-log）

> 每天花 2 分钟写一行。格式：`日期 · 学了什么 · 遇到什么问题 · 怎么解决的`。

## 模板

```
### 2026-XX-XX
- 学了：……
- 卡住：……
- 解决：……
- 明日计划：……
```

---

<!-- 从下面开始写，最新的一天放最上面 -->

### 2026-10-26
- 学了：线 B 的 L5~L7 跑通，**20 道练习全部完成**；补上「关键词/语法理解」这一课：LangChain 代码 90% 逃不出 5 种模板（创建对象 / 调方法 / 链式 / 管道 / 装饰器）；Python 执行入口在最后几行，要**从下往上读**
- 卡住：import 那 6 行看不懂，分不清类是函数还是常量；`07.py` 注释只对 2.5/5
- 解决：交付《关键词表》（40 词人话版）+《逐行拆解-07》（6 行 import 逐个拆 + 5 个模板 + 逐行讲解 + 注释点评）
- 新增：专题 27-Annotated类型标签（`Annotated[list, add_messages]` 里 add_messages 是标签不是调用）
- 明日计划：用逐行拆解重读 07.py；给 checkpointer 加跨轮记忆；修线 A 遗留 6 处 bug

### 2026-10-25
- 学了：Python 语法补齐 13 道练习全部写完（2 对 / 2 近似 / 6 待修 / 3 待验收）；确立「先学 → 后练 → 默写」规则，新增 9 节教材（`agent-lab/basics/知识点.md`）；明确 RAG 必学、NLP 只学 5 个概念
- 卡住：`apply` 少了遍历、装饰器丢了 `return result`、`field` 没导入、TypedDict 键不匹配、IDE 自动导入垃圾
- 解决：全部定位到具体行；决定先走完线 B 再统一修；安全自查确认 API Key 从未进过 GitHub（4 项检查全过）
- 其他：GitHub 用户名 `2471429249-cpu` → `bianjiaojiao`，remote 已更新并验证通过
- 产出：新增 `notes/langchain/` 独立专区（进度/踩坑/资源评估）+ 当日日记；评估教程 ai-agents-from-zero（定位：参考书，非主线）
- 明日计划：线 B L1~L7；修线 A 的 6 处 bug；重做 05b 填空练习

### 2026-10-23
- 学了：代码路线全部跑通（00 自检 / 01 调用模型 / 02 LCEL 链 / 03 工具 Agent / 04 结构化输出）；LangGraph 四概念（State/Node/Edge/条件边）；DeepSeek 是**部分** OpenAI 兼容（支持 function calling，不支持 json_schema）
- 卡住：`04_structured.py` 报 `This response_format type is unavailable now`（DeepSeek 不支持 json_schema）；`05_langgraph_agent.py` 尚未跑通
- 解决：结构化输出改 `method="function_calling"` 并实测通过；PowerShell 需 `.\` 前缀
- 产出：新增专题 26-LangGraph基础；新增长篇规划 `plans/2026-10-23-LangChain-LangGraph掌握路线.md`（7 阶段 / 12~14 周）
- 明日计划：跑通 05；给图加 checkpointer 做跨轮记忆；进阶段 1（消息体系 + LCEL 深入）

### 2026-10-22
- 学了：`dataclass` 深入（类型注解必须、`frozen=True`、`field(init=False)`、`__post_init__` 校验）；Agent 开发环境（DeepSeek 是 OpenAI 兼容 → 零插件；langchain 1.4.7 / langgraph 1.2.16）；Langflow 1.12 接 DeepSeek（原生 DeepSeek 组件 + OpenAI Compatible）
- 卡住：Langflow 里 Base URL 被填成了变量名 `OPENAI_COMPATIBLE_BASE_URL` 导致 SSRF 校验报错；连线接反导致 `Input data cannot be None`
- 解决：Base URL 改成 `https://api.deepseek.com`；搞清「左进右出」连线规则；新增 4 张截图转写 → `notes/source/2026-10-22/`；新建 3 篇专题（23~25）+ 当日日记；桌面新建 `agent-lab/` 独立环境（venv + 脚手架 + 学习路线 README）
- 明日计划：填 API Key 跑通 `00_check.py`；Langflow 练习 3（代理程序+计算器）；继续阶段测验 7~18

### 2026-10-21
- 学了：推导式（列表/字典/集合/生成器表达式）、`.items()` 解包、类型注解（参数加冒号返回加箭头）、`pathlib`（路径是对象、判断/读写/遍历/创建删除、老手口诀）、异常处理（四件套、`raise`、异常链、自定义异常、报错名清单、3 个致命坑）
- 卡住：（待填写）
- 解决：11 张新截图逐张转写 → `notes/source/2026-10-21/`；新建 4 篇主题笔记（19~22）+ 当日日记；顺手完成阶段测验第 6 题（`6.py` 用了 `pathlib`）
- 明日计划：面向对象收尾（继承/`super`/`@property`）；装饰器；补第 10 题；修 10-17 遗留 5 个 bug

### 2026-10-20
- 学了：闭包（嵌套函数 + 自由变量 + `nonlocal`、装饰器与闭包的关系、参数遮蔽坑）；线程/进程课程截图补充
- 卡住：（待填写）
- 解决：18 张新截图归档 `notes/source/2026-10-20/`（当前模型不支持读图，仅清单归档）；新建专题 `18-闭包.md` + 当日日记
- 明日计划：面向对象收尾（继承/`super`/`@property`）；补第 10 题与文件 I/O；修 10-17 遗留 5 个 bug

### 2026-10-19
- 学了：`Enum` 枚举（name/value、不能比大小→`IntEnum`、适用场景）；`for` 是最标准迭代方式；元类与 `type`（一切类源自 type、`type(类名, 父类元组, 属性字典)` 动态造类、元类是造类中转站）；类属性 vs 实例属性（共享 vs 各存各的）；线程与进程（`Thread` 的 `args`/`kwargs`、`Lock`、`Condition`、`Queue`、`Event`、线程池、多进程、GIL）
- 卡住：（待填写）
- 解决：新增 4 张截图转写 → `notes/source/2026-10-19/`；新建 4 篇主题笔记（14~17）；按文档内指令补齐线程/进程专题（含 `Condition`）
- 明日计划：面向对象收尾（继承/`super`/`@property`）；补第 10 题与文件 I/O；修 10-17 遗留 5 个 bug

### 2026-10-18
- 学了：迭代第五章 —— `while` 与真假值（6 种假值）、`match/case` 边界、函数进阶（多返回值/元组解包、可变默认参数陷阱、`lambda` 限制）、迭代器（`iter`/`next`、不可逆、`enumerate`）、特殊方法 `__eq__`/`__hash__`
- 卡住：（待填写）
- 解决：`新建 DOC 文档.doc` 新增 8 张截图全部转写归档 → `notes/source/2026-10-18/`；新建 4 篇主题笔记（10~13）+ 当日日记 `notes/daily/2026-10-18.md`
- 明日计划：迭代进阶函数；补第 10 题与文件 I/O；修 10-17 遗留 5 个 bug

### 2026-10-17
- 学了：P1 启动 —— 手写 P0 十题（1~9 完成）、`__main__` 入口、函数参数白写、f-string 格式化（千分位/对齐）、list/tuple/dict/set 容器方法、排序三参数、去重保序三写法、词频清洗顺序、生成器 yield 预热
- 卡住：第 10 题文件读写（`10.py` 只有 `def `）；文件 I/O 完全空白；`6.py` 斐波那契结果算错（`x1,x2 = x2, x1+x2` 后又 `append(x1+x2)`）
- 解决：25 张截图笔记全部转写归档（`notes/source/2026-10-17/`），知识点整理进 `notes/topics/`（9 个主题），当日记事见 `notes/daily/2026-10-17.md`；体检出 2.py 除法 `//`、4.py 未处理非法输入等 5 个问题，列入明日修复
- 明日计划：完成第 10 题；文件 I/O D1–D2（open/with/读取三法）；修 5 个 bug；LeetCode Easy 1 题

### 2026-10-13
- 学了：环境检查确认（Anaconda 3.14 / Python 3.13 / PyCharm 2025.2），跑通 py-bootcamp 10 个练习
- 卡住：（待填写）
- 解决：（待填写）
- 明日计划：把 10 个练习各手抄一遍，开始学 P1 函数与推导式
