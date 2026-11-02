import sys
from pathlib import Path

# 下面两行让脚本能找到 agent-lab 里的 config.py / .env，不用管
sys.path.insert(0, r"C:\Users\边角\Desktop\agent-lab")

import config  # 修中文乱码

from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from config import get_llm

"""Q8 · 记忆（L11）

【要求】
    1. State：messages: Annotated[list, add_messages]
    2. compile(checkpointer=MemorySaver())
    3. 同一个 thread_id 跑两轮：
         第一轮："我叫边角，我在学 LangChain"
         第二轮："我叫什么？我在学什么？"
    4. 打印第二轮回答，并打印两轮的 prompt_tokens

【验收】
    · 第二轮准确说出名字和学习内容
    · 第二轮的 prompt_tokens 明显大于第一轮

【提示】
    tokens = r["messages"][-1].response_metadata["token_usage"]["prompt_tokens"]
"""

# ↓↓↓ 在这里写 ↓↓↓
class State(TypedDict):
    messages:Annotated[list,add_messages]

def chat(state:State):
    return {"messages":get_llm().invoke(state["messages"])}
g = StateGraph(State)
g.add_node("chat",chat)
g.add_edge(START,"chat")
g.add_edge("chat",END)
app = g.compile(checkpointer = MemorySaver())
command1 = {"configurable":{"thread_id":"1"}}
command2 = {"configurable":{"thread_id":"2"}}
c2 = {"configurable":{"thread_id":"2"}}
r = app.invoke({"messages":[HumanMessage("你好,我叫边角")]},command1)
r1 = app.invoke({"messages":[HumanMessage("hello,我叫什么")]},command1)
print(r)
print(r1)
r2 = app.invoke({"messages":[HumanMessage("hello,我叫什么")]},command2)
print(r2)