
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

def get_current_cursor():
    """获取当前光标位置"""
    cursor = 4  # 光标落在 "Step B1" 这一行
    return cursor

def handler(**args):
    from parser import Parser
    from collections import defaultdict
    # ✉️ 构造邮件列表
    input_email_list = {
        "0/0": "Updated Step B1",
        "0/1": "Updated Step B2",
        "1/0": "Updated Plan A"
    }

    # 📬 构建 hook 系统（模拟简化路径）
    results = defaultdict(list)
    function_list = {
        k: (lambda c, k=k: results[k].append(cursor))
        for k in input_email_list.keys()
    }

    def set_email(emails):
        email_dict = defaultdict(dict)
        for key, fn in emails.items():
            parts = key.split("/")
            if len(parts) == 2:
                p, c = map(int, parts)
                email_dict[p][c] = fn
        return email_dict

    # 📦 注入 hook 到 parser
    parser = Parser()
    parser.stack.emails = set_email(function_list)

    # 🐾 手动构建 context 根节点
    parser.stack.context[(-999, -999)] = {"type": "context", "children": []}
    parser.stack._stack = [(-999, -999)]  # 设置根路径
    for line in lines:
        parser.parse(line)  # 修复：逐行调用 parse()
