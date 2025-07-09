import re


class Scanner:
  def __init__(self, specification, keywords):
    self.possible_tokens = specification
    self.keywords = keywords
    self.regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.possible_tokens)
    self.get_token = re.compile(self.regex).match

  def tokenize(self, code):
    tokens = []
    line = 1
    line_start = 0
    position = 0
    token = self.get_token(code, position)

    while token:
      type = token.lastgroup
      value = token.group()

      start_pos = token.start()
      end_pos = token.end()

      if type == 'NEWLINE':
        line += 1
        line_start = end_pos
      elif type in ('SKIP', 'COMMENT'):
        pass
      elif type == 'ID' and value in self.keywords:
        tokens.append({'type': 'KEYWORD', 'value': value, 'line': line})
      elif type == 'MISMATCH':
        print(f"Erro: [[{value}]], Linha {line}")
        position = end_pos
        while position < len(code) and code[position] != ';':
          position += 1
        token = self.get_token(code, position)
        continue
      else:
        tokens.append({'type': type, 'value': value, 'line': line})

      position = end_pos
      token = self.get_token(code, position)

    return tokens
