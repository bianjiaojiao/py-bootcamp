---
title: json 与数据序列化
category: 工程
keywords: [json, dumps, loads, 序列化, API, 中文乱码, ensure_ascii]
dates: [2026-11-07]
---

# json 与数据序列化

> 一句话：**把 Python 对象变成字符串（存文件/发网络），再变回来数据。**

---

## 为什么需要

**问题**：Python 的字典、列表只存在内存里。程序一关就没了，也没法通过网络发给别人。

**解决**：变成**字符串**。

```python
{"name": "边角", "age": 20}      ← Python 字典（内存里）
        ↓ json.dumps（序列化）
'{"name": "\u8fb9\u89d2", "age": 20}'   ← 字符串（能存能传）
        ↓ json.loads（反序列化）
{"name": "边角", "age": 20}      ← 又变回字典
```

**所有 API 都用这种格式**——你 F4 那个 `/ask` 接口，发出去的就是 JSON。

---

## 两个核心函数

| 函数 | 方向 | 例子 |
| --- | --- | --- |
| `json.dumps(obj)` | Python 对象 → **字符串** | `json.dumps({"a": 1})` → `'{"a": 1}'` |
| `json.loads(text)` | 字符串 → Python 对象 | `json.loads('{"a": 1}')` → `{"a": 1}` |

**记忆**：`s` 结尾的是 **s**tring（处理字符串）。

带文件的两个（顺带记）：

| 函数 | 干什么 |
| --- | --- |
| `json.dump(obj, f)` | 直接写进文件 |
| `json.load(f)` | 直接从文件读 |

> `dumps` = dump **s**tring；`dump` = 直接 dump 到文件。
> `loads` = load **s**tring；`load` = 从文件 load。

---

## 能转什么，不能转什么

| Python 类型 | JSON | 说明 |
| --- | --- | --- |
| `dict` | `{}` | ✅ |
| `list` / `tuple` | `[]` | ✅（tuple 变 list 回来） |
| `str` | `""` | ✅ |
| `int` / `float` | 数字 | ✅ |
| `True` / `False` | `true` / `false` | ✅（**首字母小写**） |
| `None` | `null` | ✅ |
| `set` | ❌ | 不支持，先转 list |
| `datetime` | ❌ | 不支持，先转字符串 |
| 自定义对象 | ❌ | 不支持，先转 dict |

---

## ⚠️ 坑 1：中文变成 `\u8fb9\u89d2`

```python
json.dumps({"name": "边角"})
# '{"name": "\\u8fb9\\u89d2"}'      ← 默认把中文转义了
```

**解决**：加 `ensure_ascii=False`

```python
json.dumps({"name": "边角"}, ensure_ascii=False)
# '{"name": "边角"}'                 ← 正常中文
```

**什么时候必须加**：存中文配置、返回给用户看的 JSON。

---

## ⚠️ 坑 2：`loads` 一个不是 JSON 的字符串 → 报错

```python
json.loads("hello")     # ❌ JSONDecodeError
json.loads("{'a': 1}")  # ❌ 单引号不是 JSON（JSON 只认双引号）
json.loads('{"a": 1}')  # ✅
```

**JSON 的规矩比 Python 严**：
- 只能用**双引号**
- 不能有尾随逗号 `[1, 2,]`
- 不能有注释

---

## ⚠️ 坑 3：转完再转回来，类型变了

```python
原数据 = (1, 2, 3)              # tuple
回来 = json.loads(json.dumps(原数据))
print(回来)                      # [1, 2, 3]  ← 变成 list 了
```

```python
原数据 = {1, 2, 3}              # set
json.dumps(原数据)               # ❌ TypeError: Object of type set is not JSON serializable
```

**记住**：JSON 只有 6 种类型（object/array/string/number/true,false/null）。**转过去再转回来，不等于原对象。**

---

## 在 RAG 项目里怎么用

```python
# ① 存配置
with open("config.json", "w", encoding="utf-8") as f:
    json.dump({"chunk_size": 200, "top_k": 3}, f, ensure_ascii=False)

# ② 存评估结果
results = [{"q": "闭包", "score": 0.7}, {"q": "线程", "score": 0.6}]
with open("eval.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)   # indent=2 好看

# ③ FastAPI 里不用手写（自动转换）
@app.post("/ask")
def ask(req: AskRequest):
    return {"answer": "...", "sources": [...]}    # ← 返回字典就自动变 JSON
```

---

## 速记卡

```
dumps  对象 -> 字符串
loads  字符串 -> 对象
dump / load  直接对文件

中文不乱码：ensure_ascii=False
好看一点： indent=2
JSON 只认双引号，只认 6 种类型
```

---

## 🔗 相关

- 文件读写：[21-pathlib路径与文件操作](21-pathlib路径与文件操作.md)
- 语法体能：[03_语法体能3.py](../../../agent-lab/03-语法训练/03_语法体能3.py) 第 5 关
- 接口开发：`agent-lab/05-工程化/F3.py`
