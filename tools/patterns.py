# 🐾 块标志
patterns = {
    'ai': 'ai:',
    'see': 'see:',
    'watch': 'watch:',
    'end': 'end',
}

# 🐾 元数据标志
data_patterns = {
    'name': 'name:',
    'date': 'date:',
}

comment_char = '```'
escape_char = '>'

# 🐾 转义行正则
ESCAPE_PATTERN = rf'^{escape_char}.*$'

# 🐾 块模式（多行块起始）
BLOCK_PATTERNS = {
    k: rf'^{comment_char}{v}(.*?)$' for k, v in patterns.items()
}
BLOCK_PATTERNS['end'] = rf'^{comment_char}{patterns["end"]}\s*$' # rewrite the end pattern

# 🐾 元数据模式（独立行）
META_PATTERNS = {
    k: rf'^{comment_char}{v}\s*(.+?)$' for k, v in data_patterns.items()
}

# 🐾 单行块模式（oneline）
ONELINE_PATTERNS = {
    k: rf'{comment_char}{v}\s*(.+?)$' for k, v in patterns.items()
}

# 🐾 inline 模式
INLINE_PATTERNS = {
    # see 模式下匹配 ai inline：连续下划线，两边空白或标点
    'ai': r'(?<=\s|[.,;!?])(_{2,})(?=\s|[.,;!?])',
    # ai 模式下匹配 see inline：[[内容]]
    'see': r'\[\[(.+?)\]\]'
}
