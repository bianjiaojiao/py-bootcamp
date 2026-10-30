# 1. 准备一个大字典（登记册）
REGISTRY = {}

# 2. 定义一个父类，里面写上魔法方法
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # cls 代表当前正在创建的那个子类
        # cls.__name__ 就是子类的名字（比如 "Dog"）
        REGISTRY[cls.__name__] = cls
        print(f"📢 自动注册成功：{cls.__name__}")


# 3. 见证奇迹！只要继承 Base，什么都不用干，自动注册
class Dog(Base):
    pass

class Cat(Base):
    pass

class Bird(Base):
    pass

# 4. 查看结果
print("\n最终的注册表：")
print(REGISTRY)