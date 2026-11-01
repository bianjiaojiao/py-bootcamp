import sys
from pathlib import Path

# 下面两行让脚本能找到 agent-lab 里的 config.py / .env，不用管
sys.path.insert(0, r"C:\Users\边角\Desktop\agent-lab")

import config  # 修中文乱码

from langchain_core.tools import tool

from config import get_llm

"""Q3 · 三个工具（L5）

【要求】
    定义三个工具（都要 @tool + 类型注解 + docstring）：
        add(a, b)            算和
        reverse_text(text)   反转字符串
        count_words(text)    数单词个数

    用 bind_tools 绑上，分别问三个问题，每次都打印 tool_calls 的 name 和 args：
        问题1：帮我算 12 加 30
        问题2：把 hello 反过来写
        问题3：这句话有几个词：i love python

【验收】
    三次输出的 name 分别是对应的工具名，args 参数正确

【提示】
    r = llm.invoke("...")
    for c in r.tool_calls:
        print(c["name"], c["args"])
"""

# ↓↓↓ 在这里写 ↓↓↓
