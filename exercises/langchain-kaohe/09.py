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
from langgraph.types import Command, interrupt

from config import get_llm

"""Q9 · 人工确认（L12）

【要求】
    1. State：messages: Annotated[list, add_messages]、sent: bool
    2. 节点里 interrupt("确认发送这封邮件吗？(yes/no)")
    3. yes  -> {"sent": True,  "messages": [("ai", "已发送")]}
       否则 -> {"sent": False, "messages": [("ai", "已取消")]}
    4. 两次 invoke：第一次看 __interrupt__，第二次用 Command(resume=...) 恢复
    5. 跑两遍：一次 yes、一次 no（用不同 thread_id）

【验收】
    · 第一次 invoke 结果里有 __interrupt__
    · 两次恢复分别得到 sent=True / sent=False

【提示】
    r1 = app.invoke({...}, config)          # 暂停
    r2 = app.invoke(Command(resume="yes"), config)   # 恢复
"""

# ↓↓↓ 在这里写 ↓↓↓
