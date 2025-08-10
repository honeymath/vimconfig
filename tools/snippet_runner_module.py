import traceback
import types

def run_code_snippets(snippets):
    """
    执行多段代码片段，返回标准化执行结果。

    参数：
        snippets (List[str]): 多个代码片段（每段如 notebook cell）

    返回：
        dict: {
            'success': bool,
            'traceback': str,            # 完整traceback信息
            'error': str or None,        # 错误类型名
            'error_message': str or None,# 错误提示
            'error_cell': int or None,   # 出错段编号（1-based）
            'error_line': int or None,   # 出错段内行号
            'error_code': str or None,   # 出错代码内容
            'stdout': str                # 如果有 print 输出（将来可重定向）
        }
    """
    combined_lines = []
    cell_line_map = []  # 每一行对应 (Cell ID, Line in Cell, Code Line)

    for idx, code in enumerate(snippets):
        cell_id = f"Cell {idx + 1}"
        lines = code.splitlines()
        for i, line in enumerate(lines, 1):
            cell_line_map.append((idx + 1, i, line))  # 用编号而非字符串
            combined_lines.append(line)

    stdout_capture = []
    result = {
        'success': True,
        'traceback': None,
        'error': None,
        'error_message': None,
        'error_cell': None,
        'error_line': None,
        'error_code': None,
        'stdout': ''
    }

    try:
        code_obj = compile("\n".join(combined_lines), filename="<snippets>", mode="exec")

        # 模拟 stdout 捕获（不依赖重定向）
        scope = {}
        exec(code_obj, scope)

    except Exception as e:
        tb = traceback.format_exc()
        last_tb = traceback.extract_tb(e.__traceback__)[-1]
        lineno = last_tb.lineno

        if 0 < lineno <= len(cell_line_map):
            cell_id, line_in_cell, code_line = cell_line_map[lineno - 1]
            result.update({
                'success': False,
                'traceback': tb,
                'error': type(e).__name__,
                'error_message': str(e),
                'error_cell': cell_id,
                'error_line': line_in_cell,
                'error_code': code_line,
            })
        else:
            result.update({
                'success': False,
                'traceback': tb,
                'error': type(e).__name__,
                'error_message': str(e),
                'error_cell': None,
                'error_line': None,
                'error_code': None,
            })

    return result

# ✅ 示例测试（临时）
if __name__ == "__main__":
    cells = [
        "a = 1\nb = 2\nc = a + b",
        "print(c)\nd = c / 0",
        "print('Done')"
    ]
    import json
    output = run_code_snippets(cells)
    print(json.dumps(output, indent=2, ensure_ascii=False))