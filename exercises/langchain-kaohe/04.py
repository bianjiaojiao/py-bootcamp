import sys
from pathlib import Path

# 下面两行让脚本能找到 agent-lab 里的 config.py / .env，不用管
sys.path.insert(0, r"C:\Users\边角\Desktop\agent-lab")

import config  # 修中文乱码

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

from config import get_llm

"""Q4 · 手动闭环（L6）

【要求】
    不许用 ToolNode，手写四步完成"算 99 乘 99"：
        1. 模型交申请单（tool_calls）
        2. 你执行工具
        3. 包装成 ToolMessage（带 tool_call_id）
        4. 发回模型拿最终回答

【验收】
    · 打印最终回答，里面包含 9801
    · 打印 .tool_calls 证明模型确实申请了工具

【提示】
    call = r.tool_calls[0]
    result = 工具.invoke(call["args"])
    msgs = [question, r, ToolMessage(content=str(result), tool_call_id=call["id"])]
"""

# ↓↓↓ 在这里写 ↓↓↓
