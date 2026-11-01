import sys
from pathlib import Path

# 下面两行让脚本能找到 agent-lab 里的 config.py / .env，不用管
sys.path.insert(0, r"C:\Users\边角\Desktop\agent-lab")

import config  # 修中文乱码

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from config import get_llm

"""Q7 · 分支图（L9）

【要求】
    1. State：question: str、answer: str
    2. 判断函数 decide(state)：
         len(state["question"]) > 15  -> 返回 "detailed"
         否则                          -> 返回 "brief"
    3. 两个模型节点：
         detailed_llm：system 里要求"详细回答，至少 3 句"
         brief_llm：   system 里要求"一句话回答，不超过 20 字"
    4. 条件边从 START 出发，两个节点都连 END

【验收】
    跑两个问题（一个长一个短），答案长度明显不同

【提示】
    g.add_conditional_edges(START, decide, {"detailed": "detailed", "brief": "brief"})
"""

# ↓↓↓ 在这里写 ↓↓↓
