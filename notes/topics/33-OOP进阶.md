---
title: OOP 进阶（property / classmethod / staticmethod / 继承 super）
category: 进阶
keywords: [property, classmethod, staticmethod, 继承, super, 描述符, 面向对象]
dates: [2026-11-08]
---

# OOP 进阶（property / classmethod / staticmethod / 继承 super）

> 四个语言机制，**不查文档也必须会**。读任何库的类都会遇到。

---

# 一、`@property` —— 把方法当属性用

## 为什么需要

```python
class Rect:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):          # 普通方法
        return self.w * self.h

r = Rect(2, 3)
r.area()      # ← 要写括号
```

**问题**：面积是"算出来的属性"，不是"动作"。写成 `r.area()` 读起来像在"执行一个动作"，很别扭。

## 加 `@property` 就变成属性

```python
class Rect:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    @property
    def area(self):          # 加了 @property
        return self.w * self.h

r = Rect(2, 3)
r.area        # 6     ← 不用写括号！
```

## 真实例子（你的项目里就有）

`course-rag/rag/qa.py:35`：

```python
@dataclass
class Answer:
    text: str
    hits: list

    @property
    def best_score(self):            # 调用时写 a.best_score
        return self.hits[0].score if self.hits else 0.0

    @property
    def sources(self):               # 调用时写 a.sources
        seen = []
        for h in self.hits:
            if h.source not in seen:
                seen.append(h.source)
        return seen
```

**`a.sources` 看起来像存好的数据，实际是每次现算的。** 这就是 `@property` 的价值：**对外像数据，对内是计算。**

---

## 三、`@property` + `.setter` —— 赋值时校验

```python
class Temp:
    def __init__(self):
        self._c = 0

    @property
    def c(self):                  # 读的时候走这里
        return self._c

    @c.setter
    def c(self, v):               # 写的时候走这里
        if v < -273:
            raise ValueError("温度不能低于绝对零度")
        self._c = v

t = Temp()
t.c = 25          # ✅ 走 setter
print(t.c)        # 25
t.c = -300        # ❌ ValueError
```

### 为什么属性名前要加 `_`

```python
self._c          # 内部变量（约定：不要直接碰）
self.c           # 对外暴露的"属性"（走 property）
```

**下划线开头 = "这是内部实现，别直接改"**（Python 没强制，是约定）。

如果没有 `_`：

```python
class Temp:
    @property
    def c(self):
        return self.c        # ← 无限递归！自己调自己，爆栈
```

---

# 二、`@classmethod` —— 备用构造器

## 为什么需要

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)              # ✅ 正常构造
p = Point.from_tuple((3, 4)) # ← 想从元组造，但没这个方法
```

**问题**：`__init__` 只接受"分开的参数"，如果你的数据是元组/字符串/字典怎么办？

## 用 `@classmethod` 造一个"备用入口"

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, t):         # cls = 类本身（注意不是 self）
        return cls(t[0], t[1])      # 等价于 Point(t[0], t[1])

p = Point.from_tuple((3, 4))
print(p.x, p.y)      # 3 4
```

## `cls` 和 `self` 的区别

| | 表示什么 | 什么时候用 |
| --- | --- | --- |
| `self` | **实例**（造出来的那个对象） | 普通方法 |
| `cls` | **类**（Point 这个类本身） | `@classmethod` |

**`@classmethod` 不需要实例就能调用**：

```python
Point.from_tuple((3, 4))     # ✅ 直接类名调用，不用先造实例
```

## 为什么用 `cls` 而不是写死 `Point`

```python
# ✅ 好：用 cls
@classmethod
def from_tuple(cls, t):
    return cls(t[0], t[1])

# ❌ 差：写死类名
@classmethod
def from_tuple(cls, t):
    return Point(t[0], t[1])
```

**区别在继承时**：

```python
class Point3D(Point):
    pass

Point3D.from_tuple((1, 2))   # ✅ 用 cls → 返回 Point3D 实例
                             # ❌ 写死 Point → 返回 Point 实例（错了！）
```

## 常见的内置 classmethod

```python
Path.cwd()              # pathlib 的类方法
dict.fromkeys([1, 2])   # 从列表造字典
str.maketrans("ab", "cd")
```

---

# 三、`@staticmethod` —— 挂类上的工具函数

## 为什么需要

有个函数**逻辑上属于这个类，但不需要用到 self 或 cls**：

```python
class MathTool:
    @staticmethod
    def add(a, b):              # 没有 self，也没有 cls
        return a + b

MathTool.add(2, 3)      # 5   ← 直接类名调用
```

## 那为什么不干脆写个普通函数？

**因为归属关系。** `add` 跟这个类有关系，放在类里**代码更好找**：

```python
MathTool.add(2, 3)      # 一看就知道"这是 MathTool 的能力"
add(2, 3)               # 这函数哪来的？
```

## 什么时候用

| 情况 | 用 |
| --- | --- |
| 需要读/改实例数据 | 普通方法（`self`） |
| 需要造实例（备用构造器） | `@classmethod`（`cls`） |
| 纯粹的工具函数，跟实例无关 | `@staticmethod` |

---

# 三种方法对比（一张表记住）

```python
class Demo:
    def normal(self):        # ① 普通方法
        ...

    @classmethod
    def c_method(cls):       # ② 类方法
        ...

    @staticmethod
    def s_method():          # ③ 静态方法
        ...
```

| | 第一个参数 | 调用方式 | 能访问实例吗 | 能访问类吗 |
| --- | --- | --- | --- | --- |
| 普通方法 | `self` | `d.normal()` | ✅ | ✅（`self.__class__`） |
| `@classmethod` | `cls` | `Demo.c_method()` | ❌ | ✅ |
| `@staticmethod` | 无 | `Demo.s_method()` | ❌ | ❌ |

---

# 四、继承 + `super()`

## 最小例子

```python
class Base:
    def __init__(self, name):
        self.info = "base:" + name

class Child(Base):
    def __init__(self, name):
        super().__init__(name)              # ← 先让父类初始化
        self.info = self.info + ":child"    # ← 再加上自己的
```

```python
Child("a").info      # "base:a:child"
```

## `super()` 到底是什么

**"找到父类，把活儿交给它。"**

```python
super().__init__(name)      # 调父类的 __init__
```

**为什么必须写**：子类的 `__init__` **不会自动调用父类的**。不写就丢了父类的初始化。

```python
class Child(Base):
    def __init__(self, name):
        self.info = "child:" + name     # ❌ 父类的初始化没执行
```

## 三种 `super()` 用法

```python
class Child(Base):
    def __init__(self):
        super().__init__()          # 调父类 __init__

    def run(self):
        return super().run()        # 调父类同名方法（先跑父类，再补充）

    @classmethod
    def make(cls):
        return super().make()       # 类方法里也能用 super()
```

## 方法重写（override）+ 扩展

```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        base = super().speak()          # 先拿父类的
        return base + " 汪汪"           # 再扩展

Dog().speak()      # "... 汪汪"
```

**这是最常见的场景**：不完全重写，而是在父类基础上加东西。

---

# 常见坑

## 坑 1：`@property` 忘了加括号调用

```python
r.area()      # ❌ TypeError: 'int' object is not callable
r.area        # ✅
```

**加了 `@property` 之后，它就不再是"方法"了。**

## 坑 2：`@property` 和 setter 名字必须一样

```python
@property
def c(self): ...

@c.setter            # ← 必须叫 c（和上面同名）
def c(self, v): ...
```

## 坑 3：在 `__init__` 里给 property 赋值

```python
class Temp:
    def __init__(self, v):
        self.c = v            # ❌ 会走 setter，如果 setter 里有校验，可能报错
        self._c = v           # ✅ 直接给内部变量
```

## 坑 4：子类忘了 `super().__init__()`

```python
class Child(Base):
    def __init__(self, name):
        self.name = name      # ❌ 父类的东西全没了
```

**症状**：`AttributeError: 'Child' object has no attribute 'info'`

## 坑 5：`@classmethod` 里用了 `self`

```python
@classmethod
def make(cls, x):
    return self.do(x)         # ❌ NameError: name 'self' is not defined
    return cls.do(x)          # ✅ 用 cls
```

---

# 速记卡

```
@property        方法变属性，调用不写括号
               配 .setter 做赋值校验
               内部变量加 _ 前缀

@classmethod   第一个参数 cls（类本身）
               用来做"备用构造器"：from_tuple / from_dict
               不写死类名（继承才对）

@staticmethod  没有 self 也没有 cls
               纯工具函数，只是放在类里好找

继承 + super   super().__init__() 必须写，否则父类初始化丢
               方法里 super().方法() 可以"先父后子"
```

---

## 🔗 相关

- 类属性与实例属性：[15-类属性与实例属性](15-类属性与实例属性.md)
- 特殊方法与哈希：[13-特殊方法与哈希](13-特殊方法与哈希.md)
- dataclass：[23-dataclass](23-dataclass.md)（`@property` 常和它一起用）
- 语法体能：[04_语法体能4.py](../../../agent-lab/03-语法训练/04_语法体能4.py) 第 1~5 关
