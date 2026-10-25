# 📚 笔记知识库（notes/）

> 这是我的 Python 学习笔记总库。**按知识点找笔记**是主入口，按日期找是辅助入口。

## ⭐ 三种阅读方式（先看这个）

| 方式 | 打开方式 | 体验 |
| --- | --- | --- |
| **① 网页书（推荐）** | 双击 [`book/Python学习笔记.html`](book/Python学习笔记.html) | 像查网页：左侧目录树点哪读哪、顶部搜索立刻定位知识点、页内小节目录、←/→ 翻页 |
| **② Word 书** | 双击 [`book/Python学习笔记.docx`](book/Python学习笔记.docx)，WPS/Word 打开 | 像翻书：**视图 → 导航窗格（大纲）** 显示一级/二级目录，点击秒跳；目录页右键「更新域」生成页码 |
| ③ Markdown 源文件 | `topics/` 目录 | 源文件，供写作/维护；日常阅读不需要看它 |

> 两本书都由 Markdown 笔记**自动生成**，内容永远一致；改完笔记重新生成即可。

## 🔁 更新流程（改完笔记后）

1. 修改/新增 `topics/`、`daily/` 里的 md 笔记
2. 双击仓库根目录的 [`一键生成笔记书.bat`](../一键生成笔记书.bat)（或命令行运行 `python notes/tools/build_book.py`）
3. 两本书自动更新，浏览器自动打开网页书

## 一、目录结构

```
notes/
├── README.md            ← 你在这里：笔记系统说明
├── INDEX.md             ← 📑 知识点总索引（自动生成，按知识点找）
├── TIMELINE.md          ← 🗓️ 学习时间线（自动生成，按日期找）
├── book/                ← ⭐ 电子书（自动生成，日常就打开这里）
│   ├── Python学习笔记.html   ← 网页书（双击即读）
│   └── Python学习笔记.docx   ← Word 书（WPS 导航窗格看目录）
├── topics/              ← 按知识点组织的笔记源文件（核心内容）
│   ├── 01-函数与程序入口.md
│   ├── 02-字符串与格式化.md
│   ├── 03-列表与元组.md
│   ├── 04-字典.md
│   ├── 05-集合.md
│   ├── 06-排序.md
│   ├── 07-去重与词频统计.md
│   ├── 08-生成器.md
│   ├── 09-类型转换.md
│   ├── 10-while循环与真假值.md
│   ├── 11-函数进阶.md
│   ├── 12-迭代器与enumerate.md
│   ├── 13-特殊方法与哈希.md
│   ├── 14-Enum枚举.md
│   ├── 15-类属性与实例属性.md
│   ├── 16-元类与type.md
│   ├── 17-线程与进程.md
│   ├── 18-闭包.md
│   ├── 19-推导式.md
│   ├── 20-类型注解.md
│   ├── 21-pathlib路径与文件操作.md
│   ├── 22-异常处理.md
│   ├── 23-dataclass.md
│   ├── 24-Agent开发环境与DeepSeek.md
│   ├── 25-Langflow基础操作.md
│   └── 26-LangGraph基础.md
├── daily/               ← 按日期组织的每日学习记录
│   ├── 2026-10-17.md
│   ├── 2026-10-18.md
│   ├── 2026-10-19.md
│   ├── 2026-10-20.md
│   ├── 2026-10-21.md
│   ├── 2026-10-22.md
│   ├── 2026-10-23.md
│   └── 2026-10-25.md
├── plans/               ← 学习计划
│   ├── 2026-10-17-后续学习与并行计划.md
│   └── 2026-10-23-LangChain-LangGraph掌握路线.md   ← ⭐ Agent 专项长篇规划
├── langchain/           ← ★ LangChain / LangGraph 独立专区（与 Python 专题分开）
│   └── README.md        ← 进度 / 踩坑 / 资源评估 / 材料索引
├── source/              ← 原始笔记素材（截图转写等）
│   ├── 2026-10-17/A.md ~ D.md
│   ├── 2026-10-18/A.md
│   ├── 2026-10-19/A.md
│   ├── 2026-10-20/A.md
│   ├── 2026-10-21/A.md
│   └── 2026-10-22/A.md
├── tools/
│   ├── build_index.py   ← 生成 INDEX.md / TIMELINE.md
│   └── build_book.py    ← 生成网页书 + Word 书
└── _templates/          ← 新笔记模板
    ├── topic.md
    └── daily.md
```

## 二、三种找笔记的方式

| 想找什么 | 去哪找 |
| --- | --- |
| **某个知识点**（如"排序"、"字典 get"） | [INDEX.md](INDEX.md) 索引名 → 点进主题文件；或直接 Ctrl+F 搜关键词 |
| **某天学了什么** | [TIMELINE.md](TIMELINE.md) 或 `daily/` 目录 |
| **按分类浏览** | `topics/` 目录（编号即学习顺序） |

## 三、如何添加新笔记（重要）

### 加一篇主题笔记（新知识点）
1. 复制 [`_templates/topic.md`](_templates/topic.md) → 粘贴到 `topics/` 下，命名如 `10-文件与IO.md`（编号接续）
2. 填写文件头的元数据（title / category / keywords / dates）
3. 写正文：知识点 + 代码示例 + ⚠️ 易错点 + 🔗 关联
4. 在仓库根目录运行自动索引：
   ```powershell
   python notes/tools/build_index.py
   ```
   （它会自动更新 `INDEX.md` 和 `TIMELINE.md`，不用手改）

### 加一篇每日记录
1. 复制 [`_templates/daily.md`](_templates/daily.md) → 粘贴到 `daily/` 下，命名如 `2026-10-18.md`
2. 填写 date / topics / summary，正文链接到当天涉及的主题笔记
3. 运行 `python notes/tools/build_index.py` 更新索引

### 加一类新分类
- 在主题文件的 `category` 里写新分类名，脚本会自动在 INDEX 里新增分组
- 推荐分类沿用：`基础结构 / 文本处理 / 容器 / 数据处理 / 进阶 / 工程 / 项目`

## 四、约定

- **主题文件是唯一权威内容**（knowledge canonical），每日记录只做"当天做了什么 + 链接到主题"
- 文件名：`编号-中文名.md`，编号决定 topics 目录顺序，也方便未来扩容
- 每篇主题笔记必须包含：一句话摘要、代码示例、⚠️ 易错点、🔗 关联
- **不要手改** `INDEX.md` / `TIMELINE.md`（它们由脚本生成，手改会被覆盖）

## 五、计划中的专题（学完即时补建）

| 专题 | 计划文件名 | 对应学习阶段 |
| --- | --- | --- |
| 面向对象（继承/多态/@property） | `26-面向对象.md` | 第 3 周 |
| 装饰器（承接闭包） | `27-装饰器.md` | 第 3 周 |
| 模块与包 | `28-模块与包.md` | 第 4 周 |
| 文件读写基础（open / with / 读取三法） | `29-文件读写.md` | 按需补 |
| 算法题笔记 | `../algorithms/`（单独目录） | 持续 |
| 项目笔记（neurocards 等） | `../projects/`（单独目录） | P1 后期 |

## 六、维护工具

```powershell
# 重建索引（INDEX.md / TIMELINE.md）
python notes/tools/build_index.py

# 重建两本电子书（网页书 + Word 书）
python notes/tools/build_book.py          # 只生成
python notes/tools/build_book.py --open   # 生成并自动打开网页书
```

也可以直接双击仓库根目录的 [`一键生成笔记书.bat`](../一键生成笔记书.bat)，它会自动按顺序重建并打开网页书。

> 两个脚本都只读笔记、只写生成物（INDEX/TIMELINE/book），不会动你的笔记正文，安全可重复运行。
> 注意：`book/` 里的两本书是生成物，不要手改；要改内容请改 `topics/`、`daily/` 里的 md，然后重新生成。
