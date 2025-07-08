from parser import Parser
from collections import defaultdict

def get_current_buffer():
    # ✨ 输入数据
    lines = [
        "#ai: Plan A",
        "Step A1",
        "#end",
        "#ai: Plan B",
        "Step B1",
        "Step B2",
        "#end",
        "Other text"
    ]
    return lines
def get_position_by_marker(marker):
    position = 8
    return position
    # ✨ 模拟获取光标位
def get_current_cursor():
    """获取当前光标位置"""
    cursor = 4  # 光标落在 "Step B1" 这一行
    return cursor

def handler(**args):
    if "marker" in args:
        marker = args["marker"]
        position = get_position_by_marker(marker)
    else:
        cursor = get_current_cursor()
        position = cursor
