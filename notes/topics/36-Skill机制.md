---
title: Skill 机制（harness 怎么调用技能）
category: 工程
keywords: [skill, SKILL.md, frontmatter, description, 上下文, harness, 触发机制]
dates: [2026-11-13]
---

# Skill 机制（harness 怎么调用技能）

> 一句话：**Skill = 一个文件夹 + 一份说明书。不是打包程序，是教模型怎么做事。**

---

## 一、最简的 skill：只有一份 SKILL.md，没有一行代码

打开本机 `json-canvas` 这个 skill，它**只有 1 个文件**：

```
C:\Users\边角\.dsh\skills\json-canvas\
└── SKILL.md        （656 行，全是"怎么写 .canvas 的 JSON 格式"）
```

**没有脚本、没有代码。** 它的作用就是：当需要生成 `.canvas` 文件时，告诉模型格式规范。

**结论：skill 可以是纯知识，不需要程序。**

---

## 二、SKILL.md 的结构：上下两半，用途完全不同

```markdown
---
name: json-canvas
description: 产品经理与内容创作者在构建 Obsidian 知识库时，
             当需要创建思维导图、流程图等可视化画布，使用此技能...
---

# JSON Canvas Skill

（正文：格式规范、字段表、示例）
```

| 部分 | 作用 | **什么时候被读** |
| --- | --- | --- |
| **frontmatter**（`---` 之间） | 什么时候该用它 | harness 启动时**只读这段** |
| **正文** | 怎么用（步骤/格式/命令） | **被选中后才读** |

---

## 三、触发流程（设计的精髓）

```
① harness 启动
   → 扫描 skills 目录
   → 每个 SKILL.md 只读 frontmatter（name + description）
   → 得到一张"能力清单"（就是系统提示里那几十个技能）

② 用户提需求："帮我做个思维导图"
   → 模型对着清单判断"json-canvas 可能有用"

③ 选中 → 这时才读 SKILL.md 正文

④ 正文里写"运行 scripts/xxx.py" → 执行脚本
```

### 为什么必须分两半

> **几十个 skill 的 description 加起来只有几千字；正文加起来几万行。**
> **只读 description 才不会撑爆上下文。**

这叫**"按需加载"**：不用的东西不占位置。

---

## 四、四种复杂度（本机真实例子）

| Skill | 文件构成 | 类型 |
| --- | --- | --- |
| `json-canvas` | **只有 `SKILL.md`（656 行）** | **纯知识**（无代码，只教格式） |
| `qwen3-tts-local` | `SKILL.md` + `scripts/tts_generator.py` + `references/voice-guide.md` | 知识 + 1 脚本 |
| `media-processor` | `SKILL.md` + **6 个脚本** + 2 个参考文档 | **工具箱**（一个 skill 装一组命令） |
| `baoyu-format-markdown` | `SKILL.md` + `.ts` + `package.json` | 带运行时依赖 |

### 两个子目录的分工

| 目录 | 装什么 | 为什么要分开 |
| --- | --- | --- |
| `scripts/` | 干活的脚本 | 正文只写"运行哪个脚本"，代码不塞进说明书 |
| `references/` | 详细资料（几百行规范） | **按需读**，不占正文 |

`media-processor` 的 SKILL.md 里就是这么列的：

```markdown
| Script | Purpose |
| --- | --- |
| image_convert.py | 转换格式（png/jpg/webp） |
| image_compress.py | 压缩体积 |
| image_scale.py | 调整尺寸 |
```

**看这张表就知道该跑哪个脚本。**

---

## 五、怎么写出能"被选中"的 description

description 决定了**会不会被用**。写不好的 skill 等于不存在。

### 好的 description 长什么样

```
产品经理与内容创作者在构建 Obsidian 知识库或梳理复杂逻辑时，
当需要创建思维导图、流程图等可视化画布，使用此技能可自动生成
标准 .canvas 文件...
```

拆开看，它有 3 个要素：

| 要素 | 例子 |
| --- | --- |
| **谁**（角色/场景） | 产品经理、内容创作者 |
| **什么时候**（触发条件） | 需要创建思维导图、流程图时 |
| **能干什么**（结果） | 自动生成标准 `.canvas` 文件 |

### 反例

```
description: 处理画布
```

**"画布"是什么？什么时候用？** 模型判断不出来 → 永远不被选中。

---

## 六、Skill 和"项目"的区别（容易混）

| | 项目（比如 course-rag） | Skill |
| --- | --- | --- |
| 是什么 | **一整套程序** | **一份说明书**（可选带脚本） |
| 谁用 | 人跑 `python xxx.py` | **模型自己读、自己跑** |
| 触发 | 你记得命令 | 你只要说出需求 |
| 位置 | 任意（`Desktop/course-rag`） | 固定：`~/.dsh/skills/<名>/` |
| 必须能跑吗 | 是 | **不一定**（纯知识 skill 没有代码） |

**关系**：一个项目可以**包一层 SKILL.md 变成 skill**。

```
course-rag（项目）                    →  ~/.dsh/skills/my-rag/
├── rag/qa.py                        ├── SKILL.md      ← "什么时候用我 + 怎么跑"
├── build_index.py                   └── scripts/
└── index.npz                            └── ask.py    ← 原项目的入口
```

---

## 七、把 RAG 包成 skill：SKILL.md 只需 4 部分

```markdown
---
name: my-rag
description: 用边角的学习笔记做检索问答。当用户问"我的笔记里讲了什么"、
             "查一下笔记"、需要基于个人笔记回答问题时使用。
---

# my-rag

## 用法
python scripts/ask.py "问题"

## 输出
- 答案正文
- 来源文件名
- 相似度分数
```

**做完之后**：用户说"查我笔记里的闭包" → 模型自动读 SKILL.md → 自动跑 `ask.py`。

---

## 八、更值得做的一种 skill：方法论

`json-canvas` 那种"纯知识 skill"说明：

> **Skill 也可以是"方法论"，不是"程序"。**

比如学完整套 RAG 之后，可以写：

```
~/.dsh/skills/rag-from-scratch/
└── SKILL.md      ← "从零搭 RAG 的 7 个阶段 + 每阶段验收标准 + 常见坑"
```

**价值**：
- 以后自己（或任何 agent）都能复用这套流程
- **能写成说明书，说明你真懂了**——这是最好的复习

---

## 速记卡

```
一个 skill = 一个文件夹 + SKILL.md
SKILL.md 分两半：
  frontmatter（name + description）→ 决定"什么时候用我"
  正文                          → 决定"怎么用我"

可选：scripts/（干活的脚本）、references/（按需读的详细资料）

触发：启动只读 description → 命中才读正文 → 正文说跑脚本才跑

description 三要素：谁 + 什么时候 + 能干什么
纯知识 skill 不需要一行代码
```

---

## 🔗 相关

- skill 目录：`C:\Users\边角\.dsh\skills\`
- 纯知识 skill 例子：`~/.dsh/skills/json-canvas/SKILL.md`（656 行，无代码）
- 工具箱 skill 例子：`~/.dsh/skills/media-processor/`（6 个脚本）
- 打包对象：[35-RAG项目架构思路](35-RAG项目架构思路.md)
- 当日记录：[2026-11-13](../daily/2026-11-13.md)
