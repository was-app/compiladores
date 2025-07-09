from pprint import pprint
from compiler.scanner import Scanner
from compiler.calibration import C
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer
from compiler.code_generator import CodeGenerator

GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_tokens(tokens):
  for token in tokens:
    token_type = token['type']
    token_value = token['value']
    token_line = token.get('line', '?')
    print(f"line: {YELLOW}{str(token_line).ljust(3)}{RESET} | type: {GREEN}{token_type.ljust(10)}{RESET} | value: {BLUE}'{token_value}'{RESET}")


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

precedence = {
    '==': 1, '!=': 1,
    '<': 2, '<=': 2, '>': 2, '>=': 2,
    '+': 3, '-': 3,
    '*': 4, '/': 4,
}

bin_op_type = {
    ('int', 'int', '+'): 'int',
    ('int', 'int', '-'): 'int',
    ('int', 'int', '*'): 'int',
    ('int', 'int', '/'): 'float',
    ('int', 'float', '+'): 'float',
    ('float', 'int', '+'): 'float',
    ('float', 'float', '+'): 'float',
    ('int', 'float', '-'): 'float',
    ('float', 'int', '-'): 'float',
    ('float', 'float', '-'): 'float',
    ('int', 'float', '*'): 'float',
    ('float', 'int', '*'): 'float',
    ('float', 'float', '*'): 'float',
    ('int', 'float', '/'): 'float',
    ('float', 'int', '/'): 'float',
    ('float', 'float', '/'): 'float',
    ('int', 'int', '>='): 'int',
    ('int', 'int', '<='): 'int',
    ('int', 'int', '>'): 'int',
    ('int', 'int', '<'): 'int',
    ('float', 'float', '>='): 'int',
    ('float', 'float', '<='): 'int',
    ('float', 'float', '>'): 'int',
    ('float', 'float', '<'): 'int',
    ('int', 'float', '>='): 'int',
    ('float', 'int', '>='): 'int',
    ('int', 'float', '<='): 'int',
    ('float', 'int', '<='): 'int',
    ('int', 'float', '>'): 'int',
    ('float', 'int', '>'): 'int',
    ('int', 'float', '<'): 'int',
    ('float', 'int', '<'): 'int',
    ('char', 'char', '=='): 'int',
    ('char', 'char', '!='): 'int',
}

assignment_compat = {
    ('int', 'int'): True,
    ('float', 'float'): True,
    ('float', 'int'): True,
    ('int', 'float'): False,
    ('char', 'char'): True,
    ('char', 'int'): False,
    ('int', 'char'): False,
    ('float', 'char'): False,
    ('char', 'float'): False,
}

file_path = 'test.c'

with open(file_path) as file:
  code = file.read()

scanner = Scanner(calibration_spec, C['KEYWORDS'])
tokens = scanner.tokenize(code)
print_tokens(tokens)
parser = Parser(tokens, precedence)
ast, symbol_table = parser.parse()

print("AST:")
pprint(ast)

print("\nTabela de símbolos:")
pprint(symbol_table)

analyzer = SemanticAnalyzer(ast, symbol_table, assignment_compat, bin_op_type)
errors = analyzer.check()
if errors:
    for e in errors:
        print(e)
else:
    print("No semantic errors.")
    cg = CodeGenerator(ast, symbol_table)
    cg.gen()




