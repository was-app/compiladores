C = {
  'KEYWORDS': {'int', 'return', 'if', 'else', 'while', 'for', 'break', 'continue', 'char', 'float', 'double', 'void', 'struct', 'typedef', 'const', 'static'},
  'COMMENT': r'//.*|/\*[\s\S]*?\*/',
  'STRING': r'"(\\.|[^"\\])*"',
  'CHAR': r"'(\\.|[^'\\])'",
  'NUMBER': r'\d+(\.\d+)?[fF]?',
  'ID': r'[A-Za-z_][A-Za-z0-9_]*',
  'OP': r'==|!=|<=|>=|&&|\|\||[-+*/%=<>&|^!~]',
  'SYMBOL': r'[{}\[\]();,]',
  'NEWLINE': r'\n',
  'SKIP': r'[ \t]+',
  'MISMATCH': r'.'
}
Cpp = {}
Python = {}
Javascript = {}
