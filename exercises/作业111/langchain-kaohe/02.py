import sys
from pathlib import Path

# 下面两行让脚本能找到 agent-lab 里的 config.py / .env，不用管
sys.path.insert(0, r"C:\Users\边角\Desktop\agent-lab")

import config  # 修中文乱码

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from config import get_llm

"""Q2 · 翻译链（L3 + L4）

【要求】
    1. 做一个 ChatPromptTemplate，三个空位：{source_lang} / {target_lang} / {text}
    2. 用 | 组装成 prompt | llm | StrOutputParser()
    3. 写函数 translate(source_lang, target_lang, text)，返回翻译结果（字符串）

【验收】
    print(translate("中文", "英文", "今天天气很好"))
    -> 直接打印英文字符串，不需要 .content

【提示】
    chain = prompt | get_llm() | StrOutputParser()
    chain.invoke({"source_lang": ..., "target_lang": ..., "text": ...})
"""

# ↓↓↓ 在这里写 ↓↓↓

# 你的 import 没问题，假设都写好了

llm = get_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译官"), # 这里的 {role} 你没传，建议直接写死或删掉
    ("human", "把 {text} 从 {source_lang} 翻译成 {target_lang}") # 👈 补上逗号
])

chain = prompt | get_llm() | StrOutputParser()

def translate(source_lang, target_lang, text):
    # 👇 必须传字典！
    return chain.invoke({
        "source_lang": source_lang,
        "target_lang": target_lang,
        "text": text
    })

# 👇 注意传参顺序：源语言，目标语言，文本
print(translate("中文", "英文", "今天天气很好"))

























