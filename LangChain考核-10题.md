# LangChain 阶段考核（L1~L13）

> 建立：2026-11-01
> 对应课表：[LangChain 从零课表](notes/plans/2026-10-31-LangChain从零课表.md)
> 关键词表：[29-LangChain基础关键词](notes/topics/29-LangChain基础关键词.md)

---

## 规则

1. **每题一个文件**，放在 `exercises/langchain-kaohe/` 下，命名 `01.py` ~ `10.py`
2. **允许**看：[29-LangChain基础关键词](notes/topics/29-LangChain基础关键词.md)、[LangChain 从零课表](notes/plans/2026-10-31-LangChain从零课表.md)
3. **不建议**看 `agent-lab/L*.py`（那是示范代码，看了就等于抄）
4. 每题都要能**独立跑通**，输出符合"验收"
5. 卡住超过 **20 分钟**就跳过，记下来问我——不要死磕

## 覆盖表

| 题 | 覆盖课次 | 核心考点 | 建议时长 |
| --- | --- | --- | --- |
| Q1 | L1 + L2 | `invoke` / `SystemMessage` / `HumanMessage` | 10 分钟 |
| Q2 | L3 + L4 | `ChatPromptTemplate` / `{变量}` / `\|` / `StrOutputParser` | 15 分钟 |
| Q3 | L5 | `@tool` / `bind_tools` / `tool_calls` 结构 | 15 分钟 |
| Q4 | L6 | `ToolMessage` / `tool_call_id` / 手动四步 | 20 分钟 |
| Q5 | L10 | `ToolNode` / `add_messages` / 循环 | 20 分钟 |
| Q6 | L7 + L8 | `StateGraph` / `add_node` / `add_edge` / 节点里调模型 | 20 分钟 |
| Q7 | L9 | `add_conditional_edges` + 判断函数 | 20 分钟 |
| Q8 | L11 | `checkpointer` / `MemorySaver` / `thread_id` | 20 分钟 |
| Q9 | L12 | `interrupt` / `Command` | 15 分钟 |
| Q10 | L13 | `.stream()` / `chunk` | 10 分钟 |

**总计约 2 小时 10 分钟。**

---

## Q1 · 角色控制（L1 + L2）

**要求**

写一个函数 `ask(role, question)`：
- 用 `SystemMessage` 把 `role` 作为规矩
- 用 `HumanMessage` 放 `question`
- 调用模型，**返回纯文字**（`str`，不是消息对象）

**验收**

```python
print(ask("只说三个字的机器人", "今天天气怎么样"))   # 输出很短，像"不知道"
print(ask("唐诗专家", "说一句关于月亮的话"))         # 输出是诗句风格
```

两句话回答风格明显不同。

---

## Q2 · 翻译链（L3 + L4）

**要求**

1. 做一个 `ChatPromptTemplate`，含三个空位：`{source_lang}`、`{target_lang}`、`{text}`
2. 用 `|` 组装成 `prompt | llm | StrOutputParser()`
3. 写一个函数 `translate(source_lang, target_lang, text)`，返回翻译结果（**字符串**）

**验收**

```python
print(translate("中文", "英文", "今天天气很好"))
# 直接打印出英文字符串，不需要 .content
```

---

## Q3 · 三个工具（L5）

**要求**

定义三个工具（都要 `@tool` + 类型注解 + docstring）：
- `add(a, b)` 算和
- `reverse_text(text)` 反转字符串
- `count_words(text)` 数单词个数

用 `bind_tools` 绑上，然后分别问三个问题，**每次都打印 `tool_calls` 里的 `name` 和 `args`**：

```
问题1：帮我算 12 加 30
问题2：把 hello 反过来写
问题3：这句话有几个词：i love python
```

**验收**

三次输出的 `name` 分别是对应的工具名，`args` 参数正确。

---

## Q4 · 手动闭环（L6）

**要求**

**不许用 `ToolNode`**，手写四步完成"算 99 乘 99"：
1. 模型交申请单（`tool_calls`）
2. 你执行工具
3. 包装成 `ToolMessage`（带 `tool_call_id`）
4. 发回模型拿最终回答

**验收**

打印最终回答，里面包含 **9801**；同时打印 `.tool_calls` 证明模型确实申请了工具。

---

## Q5 · 工具图（L10）

**要求**

1. 两个工具：`add`、`mul`
2. `State` 用 `Annotated[list, add_messages]`
3. 建图：`agent` 节点（调模型）+ `tools` 节点（`ToolNode`）+ 条件边 + **`tools` 连回 `agent`**
4. 问：`"先算 12 加 30，再算 7 乘 8"`
5. 打印每一步的消息（谁说了什么）

**验收**

能看到**两次工具调用**（或一次并行两个），最后给出最终回答。

---

## Q6 · 两节点图（L7 + L8）

**要求**

1. `State` 两个字段：`question: str`、`answer: str`
2. 节点 `ask_llm`：调模型回答 `state["question"]`，结果放进 `answer`
3. 节点 `decorate`：把 `answer` 改成 `"【答】" + answer + "【完】"`
4. 连线 `START → ask_llm → decorate → END`

**验收**

```python
print(app.invoke({"question": "什么是列表"})["answer"])
# 输出以【答】开头，以【完】结尾
```

---

## Q7 · 分支图（L9）

**要求**

1. `State`：`question: str`、`answer: str`
2. 判断函数 `decide(state)`：
   - `len(state["question"]) > 15` → 返回 `"detailed"`
   - 否则 → 返回 `"brief"`
3. 两个模型节点：
   - `detailed_llm`：system 里要求"详细回答，至少 3 句"
   - `brief_llm`：system 里要求"一句话回答，不超过 20 字"
4. 条件边从 `START` 出发，两个节点都连 `END`

**验收**

跑两个问题（一个长一个短），答案长度明显不同。

---

## Q8 · 记忆（L11）

**要求**

1. `State`：`messages: Annotated[list, add_messages]`
2. `compile(checkpointer=MemorySaver())`
3. 同一个 `thread_id` 跑两轮：
   - 第一轮：`"我叫边角，我在学 LangChain"`
   - 第二轮：`"我叫什么？我在学什么？"`
4. 打印第二轮回答，**并打印两轮的 `prompt_tokens`**（从 `response_metadata` 里取）

**验收**

- 第二轮准确说出名字和学习内容
- 第二轮的 `prompt_tokens` **明显大于**第一轮

---

## Q9 · 人工确认（L12）

**要求**

1. `State`：`messages: Annotated[list, add_messages]`、`sent: bool`
2. 节点里 `interrupt("确认发送这封邮件吗？(yes/no)")`
3. `yes` → `{"sent": True, "messages": [("ai", "已发送")]}`
4. 否则 → `{"sent": False, "messages": [("ai", "已取消")]}`
5. 两次 `invoke`：第一次看 `__interrupt__`，第二次用 `Command(resume=...)` 恢复
6. **跑两遍**：一次 yes、一次 no（用不同 `thread_id`）

**验收**

- 第一次 `invoke` 结果里有 `__interrupt__`
- 两次恢复分别得到 `sent=True` / `sent=False`

---

## Q10 · 流式（L13）

**要求**

1. 用 Q2 的翻译链（或新做一个）
2. 用 `chain.stream({...})` 逐字打印
3. 统计一共收到多少片，最后打印

**验收**

- 能肉眼看到字一个个冒出来
- 最后打印片数（比如"共 34 片"）

---

## 评分

| 完成题数 | 评价 |
| --- | --- |
| 10/10 | 优秀——可以开始做自己的 Agent 项目 |
| 8~9/10 | 良好——回头补错的那一两课 |
| 6~7/10 | 及格——重点重做 Q4、Q5、Q8（工具闭环和记忆最容易混） |
| ≤5/10 | 需要重学——建议按课表把 L5~L11 再走一遍 |

---

## 提交

10 个文件都放在 `exercises/langchain-kaohe/` 下，跑通后告诉我，我逐个 review。
