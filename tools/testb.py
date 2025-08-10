# 🐱 testb.py - 简化但完整的测试驱动脚本
# 按照 testa.py 的逻辑：输出原始lines、邮件列表、修改后的lines

from parser import Parser
from collections import defaultdict

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

cursor = 4  # 光标落在 "Step B1" 这一行

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

# 🛠️ 计算修改区域（简单模拟）
def compute_ranges(results):
    modify_ranges = []
    for k in results:
        modify_ranges.append((k, [cursor, cursor+1]))  # 简化为一行
    return modify_ranges

# 🧪 应用修改
def apply_edits(lines, modify_dict, ranges):
    new_lines = lines[:]
    for (p, c), (start, end) in zip(modify_dict, ranges):
        new_content = modify_dict[f"{p}/{c}"].split('\n')
        new_lines[start:end] = new_content
    return new_lines

ranges = compute_ranges(results)
updated_lines = apply_edits(lines, input_email_list, ranges)

# 🖨️ 输出
print("\n===== Original Lines =====")
for l in lines:
    print(l)

print("\n===== Triggered Emails =====")
for k, v in results.items():
    print(f"Path: {k}, Cursor(s): {v}")

print("\n===== Modified Lines =====")
for l in updated_lines:
    print(l)
