import sys
from pathlib import Path

# 下面两行让脚本能找到 agent-lab 里的 config.py / .env，不用管
sys.path.insert(0, r"C:\Users\边角\Desktop\agent-lab")

import config  # 修中文乱码

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from config import get_llm

"""Q6 · 两节点图（L7 + L8）

【要求】
    1. State 两个字段：question: str、answer: str
    2. 节点 ask_llm：调模型回答 state["question"]，结果放进 answer
    3. 节点 decorate：把 answer 改成 "【答】" + answer + "【完】"
    4. 连线 START -> ask_llm -> decorate -> END

【验收】
    print(app.invoke({"question": "什么是列表"})["answer"])
    -> 输出以【答】开头，以【完】结尾

【提示】
    节点只返回要改的字段：return {"answer": ...}
"""

# ↓↓↓ 在这里写 ↓↓↓
class State(TypedDict):
    question:str
    answer:str
def ask_llm(state:State):
    return {"answer": get_llm().invoke(state["question"]).content}
def decorate(state:State):
    return {"answer": f"【答】{state['answer']}【完】"}

g = StateGraph(State)
g.add_node("ask",ask_llm)
g.add_node("de",decorate)
g.add_edge(START,"ask")
g.add_edge("ask","de")
g.add_edge("de",END)
app = g.compile()
print(app.invoke({"question": "什么是列表"})["answer"])
