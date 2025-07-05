# 🐾 块标志
META = ['name', 'date']  # 元数据标志
patterns = {
    'ai': 'ai:(.*?)$',  # ai 模式
    'see': 'see:(.*?)$',  # see 模式
    'watch': 'watch:(.*?)$',  # watch 模式
    'name': 'name:(.*?)$', ## metadata
    'date': 'date:(.*?)$', ## metadata
    'end': 'end()$',
}
comment_char = '```'
escape_char = '>'
ESCAPE_PATTERN = rf'^{escape_char}.*$'
BLOCK_PATTERNS = { k: rf'^{comment_char}{v}' for k, v in patterns.items() }
ONELINE_PATTERNS = { k: rf'^(.*?){comment_char}{v}' for k, v in patterns.items() if k not in META }
INLINE_PATTERNS = { 'ai': r'(?<=\s|[.,;!?])(_{2,})(?=\s|[.,;!?])', }

if __name__ == '__main__':
    import json
    print('Available patterns:', json.dumps(patterns, indent=2))
    print('Comment character:', json.dumps(comment_char, indent=2))
    print('Escape character:', json.dumps(escape_char, indent=2))
    print('Block patterns:', json.dumps(BLOCK_PATTERNS, indent=2))
    print('Oneline patterns:', json.dumps(ONELINE_PATTERNS, indent=2))
    print('Inline patterns:', json.dumps(INLINE_PATTERNS, indent=2))
