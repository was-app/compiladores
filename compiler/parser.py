class Parser:
    def __init__(self, tokens, precedence):
        self.tokens = tokens
        self.pos = 0
        self.symbol_table = {}
        self.precedence = precedence

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def check(self, expected_type=None, expected_value=None):
        token = self.current()
        if token is None:
            raise Exception("No Token")

        if expected_type and token['type'] != expected_type:
            raise Exception(f"Expected {expected_type} but got {token['type']} at line {token['line']}")
        if expected_value and token['value'] != expected_value:
            raise Exception(f"Expected {expected_value} but got {token['value']} at line {token['line']}")

        self.pos += 1
        return token

    def parse(self):
        # could add more functions
        return self.parse_function()

    def parse_function(self):
        ret_type = self.check('KEYWORD')['value']
        name = self.check('ID')['value']
        self.check('SYMBOL', '(')
        # arguments
        self.check('SYMBOL', ')')
        self.check('SYMBOL', '{')
        body = self.parse_block()
        self.check('SYMBOL', '}')

        return {
            'type': 'FunctionDeclaration',
            'return_type': ret_type,
            'name': name,
            'params': [],
            'body': body
        }, self.symbol_table

    def parse_block(self):
        statements = []
        while self.current() and self.current()['value'] != '}':
            # treatment for loops and conditionals
            statement = self.parse_statement()
            statements.append(statement)
        return statements

    def parse_statement(self):
        token = self.current()
        if token['type'] == 'KEYWORD':
            if token['value'] == 'return':
              return self.parse_return_statement()
            else:
              return self.parse_variable_declaration()
        elif token['type'] == 'ID':
            return self.parse_atribution()
        else:
            raise Exception(f"Unsuported token in statement: {token}")

    def parse_return_statement(self):
      self.check('KEYWORD', 'return')
      expr = self.parse_expression()
      self.check('SYMBOL', ';')
      return {
          'type': 'ReturnStatement',
          'value': expr
      }

    def parse_variable_declaration(self):
        var_type = self.check('KEYWORD')['value']
        identifier = self.check('ID')
        name = identifier['value']
        line = identifier['line']
        self.check('OP', '=')
        expr = self.parse_expression()
        self.check('SYMBOL', ';')

        self.symbol_table[name] = {'type': var_type, 'line': line}

        return {
            'type': 'VariableDeclaration',
            'var_type': var_type,
            'name': name,
            'value': expr
        }

    def parse_atribution(self):
        var = self.check('ID')
        identifier = var['value']
        line = var['line']
        declared_var = self.symbol_table.get(identifier, None)
        if declared_var:
            type = declared_var.get('type')
        else:
            type = None
        self.check('OP', '=')
        expr = self.parse_expression()
        self.check('SYMBOL', ';')
        return {
            'type': 'Atribution',
            'var_type': type,
            'name': identifier,
            'value': expr
        }

    
    # Recursive
    def parse_expression(self, precedence=0):
        left = self.parse_primary()

        while True:
            op_token = self.current()
            if op_token and op_token['type'] == 'OP' and op_token['value'] in self.precedence:
                op_prec = self.precedence[op_token['value']]
                if op_prec < precedence:
                    break
                op = self.check('OP')['value']
                right = self.parse_expression(op_prec + 1)
                left = {
                    'type': 'BinaryExpression',
                    'operator': op,
                    'left': left,
                    'right': right
                }
            else:
                break

        return left

    def parse_primary(self):
      token = self.current()
      if token['type'] == 'NUMBER':
          raw_value = token['value']
          if raw_value.lower().endswith('f'):
              value = float(raw_value[:-1])
          elif 'e' in raw_value.lower() or '.' in raw_value:
              value = float(raw_value)
          else:
              value = int(raw_value)
          self.check('NUMBER')
          return {'type': 'NumberLiteral', 'value': value}
      elif token['type'] == 'STRING':  
        value = token['value']
        self.check('CHAR_LITERAL')
        return {'type': 'CharLiteral', 'value': value}
      elif token['type'] == 'ID':
          name = token['value']
          self.check('ID')
          return {'type': 'Identifier', 'name': name}
      elif token['type'] == 'SYMBOL' and token['value'] == '(':
          self.check('SYMBOL', '(')
          expr = self.parse_expression()
          self.check('SYMBOL', ')')
          return expr
      else:
          raise Exception(f"Unexpected token in expression: {token}")