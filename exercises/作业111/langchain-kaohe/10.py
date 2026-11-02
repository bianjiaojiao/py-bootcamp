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
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import get_llm

# 1. 正常的翻译链
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译官"),
    ("human", "把 {text} 从 {source_lang} 翻译成 {target_lang}")
])
chain = prompt | get_llm() | StrOutputParser()

# 2. 初始化一个计数器
chunk_count = 0

print("--- 开始流式输出 ---")
# 3. 这里把 invoke 换成 stream，参数格式一模一样
for chunk in chain.stream({"text": "今天天气很好", "source_lang": "中文", "target_lang": "英文"}):
    # 因为末尾有 StrOutputParser，所以 chunk 直接就是字符串
    print(chunk, end="", flush=True)
    chunk_count += 1 # 每接到一片，计数器加 1

print() # 循环结束后，打印个换行
print(f"\n✅ 接收完毕，共收到 {chunk_count} 片")