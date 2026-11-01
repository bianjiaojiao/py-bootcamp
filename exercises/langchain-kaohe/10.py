import sys
from pathlib import Path

# 下面两行让脚本能找到 agent-lab 里的 config.py / .env，不用管
sys.path.insert(0, r"C:\Users\边角\Desktop\agent-lab")

import config  # 修中文乱码

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from config import get_llm

"""Q10 · 流式（L13）

【要求】
    1. 做一个翻译链（或任意 chain）
    2. 用 chain.stream({...}) 逐字打印
    3. 统计一共收到多少片，最后打印

【验收】
    · 能肉眼看到字一个个冒出来
    · 最后打印片数（比如"共 34 片"）

【提示】
    for chunk in chain.stream({...}):
        print(chunk, end="", flush=True)   # chain 出来的直接是字符串
"""

# ↓↓↓ 在这里写 ↓↓↓
