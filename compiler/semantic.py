class SemanticAnalyzer:
    def __init__(self, ast, symbol_table, assignment_compat, bin_op_type):
        self.ast = ast
        self.symbol_table = symbol_table
        self.errors = []
        self.assignment_compat = assignment_compat
        self.bin_op_type = bin_op_type

    def error(self, msg, line=None):
        if line is not None:
            self.errors.append(f"[Line {line}] Semantic error: {msg}")
        else:
            self.errors.append(f"Semantic error: {msg}")

    def check(self):
        declared_vars = {}
        body = self.ast.get('body', [])
        # only function body for now

        for statement in body:
            if statement['type'] == 'VariableDeclaration':
                name = statement['name']
                var_type = statement['var_type']
                line = self.symbol_table.get(name, {}).get('line', None)

                if name in declared_vars:
                    self.error(f"Variable {name} redeclared", line)
                else:
                    declared_vars[name] = var_type

                expr_type = self.get_expr_type(statement['value'], declared_vars, line)
                if expr_type is None:
                    self.error(f"No type to assign to {name}", line)
                else:
                    can_assign = self.assignment_compat.get((var_type, expr_type), False)
                    if not can_assign:
                        self.error(f"Can't assign {expr_type} to variable {name} of type {var_type}", line)

            elif statement['type'] == 'ReturnStatement':
                self.get_expr_type(statement['value'], declared_vars)
            elif statement['type'] == 'Atribution':
                name = statement['name']
                var_type = statement['var_type']
                line = self.symbol_table.get(name, {}).get('line', None)

                if name not in declared_vars:
                    self.error(f"Variable {name} not declared", line)
                
                expr_type = self.get_expr_type(statement['value'], declared_vars)
                if expr_type is None:
                    self.error(f"No type to atribute to {name}", line)
                else:
                    can_assign = self.assignment_compat.get((var_type, expr_type), False)
                    if not can_assign:
                        self.error(f"Can't assign {expr_type} to variable {name} of type {var_type}", line)

        return self.errors

    def get_expr_type(self, expr, declared_vars, line=None):
        etype = expr.get('type')

        if etype == 'NumberLiteral':
            val = expr.get('value')
            if isinstance(val, int):
                return 'int'
            elif isinstance(val, float):
                return 'float'
            else:
                return None

        elif etype == 'Identifier':
            name = expr.get('name')
            if name not in declared_vars:
                self.error(f"Use of undeclared variable {name}", line)
                return None
            return declared_vars[name]

        elif etype == 'BinaryExpression':
            left_type = self.get_expr_type(expr['left'], declared_vars, line)
            right_type = self.get_expr_type(expr['right'], declared_vars, line)
            op = expr['operator']

            if left_type is None or right_type is None:
                return None

            result_type = self.bin_op_type.get((left_type, right_type, op))
            if result_type is None:
                self.error(f"Invalid operation ({left_type} {op} {right_type})", line)
                return None
            return result_type

        else:
            self.error(f"Unknown expression type {etype}", line)
            return None
