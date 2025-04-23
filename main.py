from scanner.scanner import Scanner
from scanner.calibration import C

GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_tokens(tokens):
  for token in tokens:
    token_type = token['type']
    token_value = token['value']
    print(f"type:  {GREEN}{token_type.ljust(10)}{RESET} | value: {BLUE}'{token_value}'{RESET}")

calibration_spec = [
    ('COMMENT', C['COMMENT']),
    ('STRING', C['STRING']),
    ('CHAR', C['CHAR']),
    ('NUMBER', C['NUMBER']),
    ('ID', C['ID']),
    ('OP', C['OP']),
    ('SYMBOL', C['SYMBOL']),
    ('NEWLINE', C['NEWLINE']),
    ('SKIP', C['SKIP']),
    ('MISMATCH', C['MISMATCH']),
]

file_path = 'test.c'

with open(file_path) as file:
  code = file.read()

scanner = Scanner(calibration_spec, C['KEYWORDS'])
tokens = scanner.tokenize(code)

print_tokens(tokens)
