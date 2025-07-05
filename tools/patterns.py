# 🐾 块标志
meta_char = ['name', 'date']  # 元数据标志
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
# 🐾 块模式（多行块起始）
BLOCK_PATTERNS = { k: rf'^{comment_char}{v}' for k, v in patterns.items() }
ONELINE_PATTERNS = { k: rf'{comment_char}{v}' for k, v in patterns.items() }
# 🐾 inline 模式, delete the see part
INLINE_PATTERNS = { 'ai': r'(?<=\s|[.,;!?])(_{2,})(?=\s|[.,;!?])', }
