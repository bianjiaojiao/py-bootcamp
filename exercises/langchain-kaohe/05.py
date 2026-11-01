import sys
from pathlib import Path

# 下面两行让脚本能找到 agent-lab 里的 config.py / .env，不用管
sys.path.insert(0, r"C:\Users\边角\Desktop\agent-lab")

import config  # 修中文乱码

from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from config import get_llm

"""Q5 · 工具图（L10）

【要求】
    1. 两个工具：add、mul
    2. State 用 Annotated[list, add_messages]
    3. 建图：agent 节点（调模型）+ tools 节点（ToolNode）+ 条件边 + tools 连回 agent
    4. 问："先算 12 加 30，再算 7 乘 8"
    5. 打印每一步的消息（谁说了什么）

【验收】
    能看到两次工具调用（或一次并行两个），最后给出最终回答

【提示】
    g.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    g.add_edge("tools", "agent")     <- 这条就是循环
"""

# ↓↓↓ 在这里写 ↓↓↓
