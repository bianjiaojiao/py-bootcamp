# Python 学习笔记 · 截图转写（2026-10-29 新增部分）

> 来源：`py-bootcamp/新建 DOC 文档.doc`（累积文档，本次共 **87** 张截图）。
> 前 70 张已在前几次转写完成，本次新增 **17 张**（image71 ~ image87）。
>
> 今日截图主题：**属性操作三兄弟 / 字典 get / 字符串方法 / enumerate / 真假值 / 生成器 / 二维列表**
> —— 都是这几天 drills 和测验里实际用到的知识点，以及自己做对的填空答案。

> 转写约定
> - 代码逐字保留：缩进、空行、符号、引号一律按原图照抄。
> - 图中有手写文字时，单独用「手写正文」标出。
> - 图中被裁切的残缺行、排版差异，用「转写说明」标出。

---

## 手写正文（第 38~40 段）

**P38**
```
file:/C:/Users/边角/Desktop/agent-lab/basics/题目.md
get_type_hints 只能作用于函数或类
```

**P39**
```
当某个函数运行后弹错误 is not defined，大概是没调用
```

**P40**
```
getattr(obj, "属性名", 默认值) —— 不知道属性在不在时用这个。
```

**P42**
```
Key = len，传递函数 len 给 sorted，让它在排序时使用
```

---

## 图 image71

知识点：**属性操作三兄弟**——平时写的 `obj.name` 是写死属性名，属性名在运行时才知道时要用这三个函数。

### 是什么

平时写 `obj.name` 是**写死**属性名。但有时属性名是**运行时才知道的**（存在变量里），这时要用三兄弟：

| 函数 | 作用 |
| --- | --- |
| `getattr(obj, "名字", 默认值)` | 取属性；**不存在时返回默认值而不报错** |
| `hasattr(obj, "名字")` | 判断有没有这个属性，返回 True/False |
| `setattr(obj, "名字", 值)` | 设置属性（等同 `obj.名字 = 值`） |

---

## 图 image72

知识点：**`字典.get(键, 默认值)` 的两个参数**。

```python
字典.get(键, 默认值)
```

- **参数 1：键（key）**。你想去字典里找的名字。
- **参数 2：默认值（可选）**。如果没找到这个键，你想让程序返回什么。如果不写，默认返回 `None`。

---

## 图 image73

知识点：**LangChain 管道符的三板斧**（记忆口诀）。

### 🚀 终极记忆

在 LangChain 的管道符 `|` 语法里，这三板斧是标配：

**提示词模板（`prompt` ➡️ 大模型（`llm`）➡️ 文本解析器（`StrOutputParser`）**

以后只要你想让大模型直接吐**人能读的纯文本**，尾巴上永远挂个 `StrOutputParser()` 就对了！

---

## 图 image74

知识点：06b 记忆填空的**第 2 空答案**——编译时传存档器。

填空提示（原图注释区）：
```
填空 2：编译时传什么，图才会"记住"历史？
        提示：导入里有一个"存档器"类，要创建它
```

答案：
```python
app = g.compile(MemorySaver())
```

---

## 图 image75

知识点：07b 人工确认填空的**第 3 空答案**——恢复执行。

填空提示（原图注释区）：
```
填空 3：恢复执行时，要用哪个类把"回答"包起来？
        写法：Xxx(resume="yes")
        提示：import 里已经导入了
```

答案：
```python
result = app.invoke(Command(resume="yes"), config)
```

---

## 图 image76

知识点：07b 人工确认填空的**第 1 空答案**——让图暂停。

填空提示（原图注释区）：
```
填空 1：调用哪个函数能让图"暂停并等人回答"？
        它会把问题抛出去，返回值就是用户的回答
```

答案：
```python
answer = interrupt({"question": "要删除 3 个文件吗？(yes/no)"})
```

---

## 图 image77

知识点：**`input()` 拿到的是字符串**，转整数前要先转浮点（处理带小数点的输入）。

> 原因在于 `input` 输入是字符串，而字符串不能直接转换成整数，需要先转换成浮点数再转化成整数。

---

## 图 image78

知识点：**`.capitalize()` 与 `.title()` 的区别**（长得很像，但处理句子里每个词的方式不同）。

### 1. `.capitalize()`：只把整句话的第一个字母大写，其余全变小写

```python
text = "hello WORLD! this is python."
print(text.capitalize())
# 输出: Hello world! this is python.
```

**注意**：不仅第一个字母大写了，后面的 `WORLD` 也被强行改成了小写 `world`。

### 2. `.title()`：把每个单词的首字母都大写

```python
text = "hello WORLD! this is python."
print(text.title())
# 输出: Hello World! This Is Python.
```

**注意**：它会把空格、标点符号后面的字母都当成新单词的开头，统统大写（但要注意，像 `it's` 会被切成 `It'S`，这是它的一个小坑）。

---

## 图 image79

知识点：**字符串去空格的四个方法 + 切分拼接**。

```
.strip()  --- 删除两边空格

.lstrip() --- 删除左边空格

.rstrip() --- 删除右边空格

.replace(" ","") --- 删除所有空格

.split() --- 先切分， "".join() --- 再拼接
```

---

## 图 image80

知识点：drills/02 第 9 关的**答案**——`sorted` + `key` + 切片。

题目（原图注释）：
```
# 第 9 关：排序（sorted + key + 切片）
# 写 top_n(words: list[str], n: int) -> list[str]
# 按【长度从长到短】排序，取前 n 个
# 提示：sorted(words, key=len, reverse=True)[:n]
```

答案：
```python
def top_n(words: list[str], n: int) -> list[str]:
    return sorted(words, key=len, reverse=True)[:n]
```

---

## 图 image81

知识点：**`enumerate` 循环里 i 和 x 分别是什么**。

```python
for i, x in enumerate(nums):
    # 第一次循环: i=0, x=10
    # 第二次循环: i=1, x=20
    # 第三次循环: i=2, x=30
    print(f"索引是{i}, 值是{x}")
```

---

## 图 image82

知识点：**`enumerate` 的本质**——每次吐出一个 `(索引, 元素)` 元组。

`enumerate` 的意思是"枚举"。当你把列表交给它，它在循环时，每次会吐出一个**元组**：`（索引，元素）`。

```python
nums = [10, 20, 30]
# 如果你只用一个变量接，拿到的是个元组
for item in enumerate(nums):
    print(item)
# 输出:
# (0, 10)
# (1, 20)
# (2, 30)
```

---

## 图 image83

知识点：**`if not w:` 的真假值判断**——Python 把"空的东西"都当 False。

一句话解释：`if not w:` 的意思是"**如果 `w` 是空的**"。

在 Python 里，`not` 是一个逻辑取反词。除了 `False` 之外，Python 把很多"**空的东西**"或"**零**"都当成 `False`。

所以，当 `w` 是以下这些情况时，`if not w:` 都会成立（变成 `True`）：

- `w = ""`（空字符串）
- `w = []`（空列表）
- `w = 0`（数字零）
- `w = None`（空值）

---

## 图 image84

知识点：**生成器 `squares(n)` + "只能迭代一次"的验证代码**（drills/02 第 8 关思路的实测）。

```python
def squares(n):
    for i in range(1, n + 1):
        yield i * i


# ================= 验证 1：用 for 遍历打印 =================
print("--- 第一次遍历（for循环）---")
for num in squares(5):
    print(num, end=" ")
print("\n")

# ================= 验证 2：生成器只能迭代一次 =================
print("--- 验证生成器是一次性耗材 ---")
gen = squares(5)        # 创建了一个生成器对象

# 第一次转换成 list
first_list = list(gen)
print(f"第一次 list()：{first_list}")

# 第二次转换成 list（注意：用的还是刚才那个 gen）
second_list = list(gen)
print(f"第二次 list()：{second_list}")

# 验证结果
if first_list and not second_list:
    print("✅ 验证成功：同一个生成器第二次迭代是空的（它被抽干了）！")
```

---

## 图 image85

知识点：**用 `append` 构造二维列表**——每次 append 一个**整个列表**。

```python
name = ['Niumei', 'YOLO', 'Niu Ke Le', 'Mona']
food = ["pizza", "fish", "potato", "beef"]
number = [3, 6, 0, 3]
friend = []
friend.append(name)
friend.append(food)
friend.append(number)
```

---

## 图 image86

知识点：**二维列表是怎么形成的** + 一个新手坑。

### 🧠 灵魂复盘：它是怎么变成二维的？

你可以把 `friends = []` 想象成一个**空的书架**。

- 第一次 `friends.append(name)`，你把"名字"这一排书放进了书架的**第 1 层**。此时书架变成了 `[['Niumei', ...]]`。
- 第二次 `friends.append(food)`，你把"食物"这一排书放进了书架的**第 2 层**。此时书架变成了 `[['Niumei', ...], ['pizza', ...]]`。
- 第三次 `friends.append(number)`，你把"数字"这一排书放进了书架的**第 3 层**。

因为 `append` 是把**整个列表**作为一个元素加进去，所以里面嵌套了列表，就变成了二维列表。

### 🚨 新手极易踩的一个坑

**千万别把元素直接 append 进去！**

如果你写成：

```python
friends.append('Niumei')   # ❌ 这样 friends 就变成一维的了
```

你必须把**整个一维列表**（比如 `name`）作为一个**整体**塞进去，才能形成二维结构。这就好比你搬家，是整箱整箱地搬，而不是把箱子拆了把衣服一件件塞进车。

---

## 图 image87

知识点：**`"".join()` 的三个硬性限制**（终极总结·必背）。

### 🎯 终极总结（必背）

- `"".join(列表)` **只能用于纯字符串列表**（如 `["a", "b"]`）。
- 如果列表里是数字，必须先用 `map(str, 列表)` 把数字全洗成字符串。
- 如果你想要**保留前导零**，结果必须是**字符串**。只要敢用 `int()` 强转，前导零必死。

---

## 本次涉及的专题

| 截图 | 对应专题 |
| --- | --- |
| image71 | [28-getattr与属性操作](../../topics/28-getattr与属性操作.md)（新增） |
| image72 | [04-字典](../../topics/04-字典.md) |
| image73 | [LangChain 完全参考手册](../../langchain/01-LangChain完全参考手册.md) |
| image74~76 | [26-LangGraph基础](../../topics/26-LangGraph基础.md) |
| image77 | [09-类型转换](../../topics/09-类型转换.md) |
| image78~79 | [02-字符串与格式化](../../topics/02-字符串与格式化.md) |
| image80、81、82 | [12-迭代器与enumerate](../../topics/12-迭代器与enumerate.md) |
| image83 | [10-while循环与真假值](../../topics/10-while循环与真假值.md) |
| image84 | [08-生成器](../../topics/08-生成器.md) |
| image85~86 | [03-列表与元组](../../topics/03-列表与元组.md) |
| image87 | [02-字符串与格式化](../../topics/02-字符串与格式化.md) |
