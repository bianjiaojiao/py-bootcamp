import sys
from pathlib import Path

# 下面两行让脚本能找到 agent-lab 里的 config.py / .env，不用管
sys.path.insert(0, r"C:\Users\边角\Desktop\agent-lab")

import config  # 修中文乱码

from langchain_core.messages import HumanMessage, SystemMessage

from config import get_llm

"""Q1 · 角色控制（L1 + L2）

【要求】
    写一个函数 ask(role, question)：
        · 用 SystemMessage 把 role 作为规矩
        · 用 HumanMessage 放 question
        · 调用模型，返回【纯文字】（str，不是消息对象）

【验收】
    print(ask("只说三个字的机器人", "今天天气怎么样"))   -> 很短，像"不知道"
    print(ask("唐诗专家", "说一句关于月亮的话"))         -> 诗句风格
    两句回答风格明显不同

【提示】
    llm.invoke([SystemMessage(...), HumanMessage(...)]).content
"""

# ↓↓↓ 在这里写 ↓↓↓
