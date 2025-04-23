from scanner import Scanner

GREEN = '\033[92m'  # Green for 'type'
BLUE = '\033[94m'   # Blue for 'value'
RESET = '\033[0m'   # Reset color

def print_colored_tokens(tokens):
    for token in tokens:
        token_type = token['type']
        token_value = token['value']
        print(f"type:  {GREEN}{token_type.ljust(10)}{RESET} | value: {BLUE}'{token_value}'{RESET}")

token_specification = [
    ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),
    ('STRING', r'"(\\.|[^"\\])*"'),
    ('CHAR', r"'(\\.|[^'\\])'"),
    ('NUMBER', r'\d+(\.\d*)?([eE][+-]?\d+)?[fF]?|\.\d+([eE][+-]?\d+)?[fF]?'),
    ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('OP', r'==|!=|<=|>=|&&|\|\||[-+*/%=<>&|^!~]'),
    ('SEPARATOR', r'[{}\[\]();,]'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
  ]

keywords = { 'int', 'return', 'if', 'else', 'while', 'for', 'break', 'continue', 'char', 'float', 'double', 'void', 'struct', 'typedef', 'const', 'static'}
file_path = 'test.c'

with open(file_path) as file:
  code = file.read()

scanner = Scanner(token_specification, keywords)


tokens = scanner.tokenize(code)

print_colored_tokens(tokens)
