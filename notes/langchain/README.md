# LangChain / LangGraph 独立学习专区

> **为什么单独放**：Python 基础专题（`topics/01~26`）是"语言能力"，LangChain/LangGraph 是"框架能力"。
> 两者性质不同、更新节奏不同，混在一起会让 `topics/` 的编号失去意义。
> 所以：**Python 笔记照旧，LangChain 全部收在这里。**

---

## 一、材料在哪

### 已归档进笔记库（本目录）

| 文档 | 内容 |
| --- | --- |
| [01-关键词表](01-关键词表.md) | 两张全景图 + 40 个词的人话解释 + 读代码三遍法 |
| [02-逐行拆解-07](02-逐行拆解-07.md) | 6 行 import 逐个拆（类/函数/常量）+ 5 个代码模板 + 逐行讲解 |
| [03-知识点补充](03-知识点补充.md) | A1~B5 共 9 节先学教材 |
| [04-学习路径](04-学习路径.md) | 两条线的时间表与验收标准 |

### 留在工作区（可运行）

| 内容 | 位置 |
| --- | --- |
| Python 语法练习（13 题） | `agent-lab/basics/题目.md` |
| Python 参考答案 | `agent-lab/basics/参考答案.py` |
| LangChain 练习（7 题） | `agent-lab/basics/题目-LangChain.md` |
| LangChain 参考答案 | `agent-lab/basics/参考答案-LangChain.py` |
| 你的作答（`01.py`~`07.py` 等） | `agent-lab/basics/` |
| 实践脚本（01~06） | `agent-lab/` |

> **分工**：**笔记库 = 知识归档（会进 git / GitHub / 电子书）；`agent-lab` = 工作区（跑代码、写练习）。

---

## 二、学习原则（血泪总结）

1. **先学后练**：笔记里没有的知识点，先读教材再做
2. **填空优先**：不要一上来从零写，先填词 → 再默写
3. **能跑通 ≠ 写对了**：TypedDict、类型注解运行时都不校验
4. **记模式不记拼写**：记"State→node→edge→compile→invoke"的顺序，import 路径交给 IDE
5. **间隔重复**：一周后回头重做，才算真记住

---

## 三、进度

### 线 A · Python 中级语法（13 题）

| 题 | 状态 | 备注 |
| --- | --- | --- |
| 01 函数当参数 | ❌ 待修 | 少了遍历 |
| 02 闭包 | ✅ 通过 | |
| 03 装饰器 | ❌ 待修 | 丢了 `return result` |
| 04 注解 | ✅ 基本通过 | `greet` 应 `-> None` |
| 05 容器注解 | ⚠️ 待清理 | 多了一行 `from pygame import key` |
| 06 dataclass | ❌ 待修 | 少 import `field` |
| 07 TypedDict | ❌ 待修 | 键与定义不匹配 |
| 08 Annotated | ❌ 待修 | 缺 `def`，未完成 |
| 09~13 | ⬜ 待验证 | 已写，未逐一验收 |

### 线 B · LangChain 语法（7 题）

| 题 | 状态 |
| --- | --- |
| L1 invoke | ⬜ 待做 |
| L2 提示词模板 | ⬜ 待做 |
| L3 LCEL 管道 | ⬜ 待做 |
| L4 工具 | ⬜ 待做 |
| L5 结构化输出 | ⬜ 待做 |
| L6 最小图 | ⬜ 待做 |
| L7 工具循环 | ⬜ 待做 |

### 总体阶段（对照长篇规划）

```
✅ 阶段 0  基础打通（调用模型 / 提示词 / 结构化 / 工具 / 首图）
🔄 阶段 0.5 语法补齐（线 A 完成待修，线 B 进行中）
⬜ 阶段 1  LangChain 核心（消息体系 / LCEL 深入）
⬜ 阶段 2  工具与 Agent
⬜ 阶段 3  LangGraph 深入（interrupt / 记忆 / 子图）
⬜ 阶段 4  RAG
⬜ 阶段 5  工程化与部署
⬜ 阶段 6  高级模式
⬜ 阶段 7  项目集整合
```

---

## 四、踩坑记录（会持续累积）

| 日期 | 坑 | 解法 |
| --- | --- | --- |
| 10-23 | `with_structured_output` 报 `This response_format type is unavailable now` | DeepSeek 不支持 `json_schema`，改 `method="function_calling"` |
| 10-23 | PowerShell 里运行当前目录程序报"无法加载模块" | 必须加 `.\` 前缀（cmd 不需要） |
| 10-24 | 练习文件在子目录，`from config import ...` 报 ModuleNotFoundError | 文件开头加 3 行 `sys.path.insert` 把上级目录加入搜索路径 |
| 10-24 | `StrOutputParser` 返回类型不是 `str` 而是 `TextAccessor` | 新版行为；用 `isinstance(out, str)` 判断（True） |
| 10-25 | 子进程里 `get_state` 查空线程 → `KeyError: 'messages'` | 空线程 `values` 是空字典，用 `.get("messages", [])` |

---

## 五、资源评估

### 《AI 智能体实战速成指南：从零到企业级落地》

- 在线：<https://didilili.github.io/ai-agents-from-zero/#/>
- 源码：<https://github.com/didilili/ai-agents-from-zero>

**定位判断：当参考书 / 拓展读物，不当主线教材。**

**优点**

| 项 | 说明 |
| --- | --- |
| 覆盖面完整 | 从大模型基础 → 提示词 → RAG → Coze/Dify → LangChain → LangGraph → MCP/A2A → 微调 → 企业项目 |
| 技术栈对口 | **Python + LangChain + LangGraph**（不是 Java 路线），和你现在走的路一致 |
| 有可运行源码 | 两个完整项目：电商问数（NL2SQL）、深度研搜（DeepAgents 多智能体） |
| 有面试题库 | 按岗位能力域组织，后期求职时有用 |
| 章节对应精准 | 第 13/14/15/17/22~25 章正好对应你正在学的知识点 |

**缺点 / 风险**

| 项 | 说明 |
| --- | --- |
| **节奏太快** | 名字就叫"速成"，27 章概念 + 6 章微调，零基础容易"看完但写不出" |
| **版本可能不匹配** | 教程可能基于 LangChain 0.3 写法，你装的是 1.4.7，部分代码照抄会报错 |
| **后期项目工程量大** | MySQL / Qdrant / Elasticsearch / Docker / RAGFlow / MinerU，对新手是不小的门槛 |
| **微调章节需要 GPU** | AutoDL 租显卡，现在完全用不上 |
| **来源是培训课整理** | 作者自述参考尚硅谷课程，章节质量可能不齐；官方文档仍是权威 |
| **宣传口吻重** | "地表最强""全网首个"这类话，打折听 |

**怎么用它（按你现在的进度）**

| 你在学什么 | 去读哪章 |
| --- | --- |
| L2 提示词模板 | 第 13 章 提示词与消息模板 |
| L3 LCEL 管道 | 第 15 章 LCEL 与链式调用 |
| L4 工具 | 第 17 章 Tools 工具调用 |
| L5 结构化输出 | 第 14 章 输出解析器 |
| L6/L7 建图 | 第 22~24 章 LangGraph（概述 / 图与状态 / 节点边） |
| 下一步 interrupt | 第 25 章 LangGraph 高级特性 |
| 阶段 4 RAG | 第 18~19 章（向量库与 Embedding / RAG） |
| 求职准备 | 面试题库 |

**不要现在做的事**

- ❌ 不要 clone 整个仓库（几百 MB）
- ❌ 不要按它的顺序从头读到尾
- ❌ 不要现在碰 Coze/Dify/微调章节
- ✅ 只做"卡住时按上表查对应章节"
