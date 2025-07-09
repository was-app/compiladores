class CodeGenerator:
    def __init__(self, ast, symbol_table):
        self.ast = ast
        self.symbol_table = symbol_table
        self.output = []
        self.offsets = {}
        self.current_offset = 0
        self._label_count = 0
        self.float_literals = {}   # mapeia valor -> rótulo
        self.data_section = []

    def gen(self, filename="compiled.s"):
        self.collect_float_literals(self.ast)

        if self.data_section:
            self.output.append(".section .data")
            self.output.extend(self.data_section)

        self.output.append(".section .text")
        self.output.append(".globl main")
        self.output.append("main:")
        self.output.append("    push %ebp")
        self.output.append("    mov %esp, %ebp")

        # Aloca espaço para variáveis
        self.allocate_stack_space()

        # Gera código para corpo da função
        for statement in self.ast['body']:
            self.gen_statement(statement)

        # Epílogo da função
        self.output.append("    mov %ebp, %esp")
        self.output.append("    pop %ebp")
        self.output.append("    ret")

        code = "\n".join(self.output)
        with open(filename, "w") as f:
            f.write(code)

    def allocate_stack_space(self):
        var_names = list(self.symbol_table.keys())
        var_names.sort()
        for name in var_names:
            self.current_offset += 4
            self.offsets[name] = self.current_offset
        self.output.append(f"    sub ${self.current_offset}, %esp    # espaço para variáveis locais")

    def collect_float_literals(self, node):
        if isinstance(node, dict):
            if node.get("type") == "NumberLiteral" and isinstance(node["value"], float):
                val = node["value"]
                if val not in self.float_literals:
                    label = f"float_{len(self.float_literals)}"
                    self.float_literals[val] = label
                    self.data_section.append(f"{label}: .float {val}")
            for key in node:
                self.collect_float_literals(node[key])
        elif isinstance(node, list):
            for item in node:
                self.collect_float_literals(item)

    def gen_statement(self, statement):
        stype = statement['type']
        if stype == 'VariableDeclaration':
            self.gen_expression(statement['value'])
            offset = self.offsets[statement['name']]
            dtype = self.symbol_table[statement['name']]['type']
            if dtype == 'float':
                self.output.append(f"    movss %xmm0, -{offset}(%ebp)    # {statement['name']}")
            else:
                self.output.append(f"    movl %eax, -{offset}(%ebp)    # {statement['name']}")

        elif stype == 'ReturnStatement':
            self.gen_expression(statement['value'])
        elif stype == 'Atribution':
          self.gen_expression(statement['value'])
          offset = self.offsets.get(statement['name'])
          dtype = self.symbol_table[statement['name']]['type']
          
          if offset is None:
              self.output.append(f"    # ERRO: variável '{statement['name']}' não encontrada")
          else:
              if dtype == 'float':
                  self.output.append(f"    movss %xmm0, -{offset}(%ebp)    # {statement['name']} (float assign)")
              else:
                  self.output.append(f"    movl %eax, -{offset}(%ebp)    # {statement['name']} (int assign)")
        else:
            self.output.append(f"    # Ignorando statement tipo {stype}")


    def gen_expression(self, expr):
        etype = expr['type']

        if etype == 'NumberLiteral':
            val = expr['value']
            if isinstance(val, int):
                self.output.append(f"    movl ${val}, %eax")
            else:
                label = self.float_literals[val]
                self.output.append(f"    movss {label}, %xmm0")

        elif etype == 'CharLiteral':
            char_value = ord(expr['value'])
            self.output.append(f"    movl ${char_value}, %eax    # char literal '{expr['value']}'")

        elif etype == 'Identifier':
            name = expr['name']
            offset = self.offsets.get(name)
            dtype = self.symbol_table.get(name, {}).get("type")
            if offset is None:
                self.output.append(f"    # ERRO: variável '{name}' não encontrada")
                self.output.append(f"    movl $0, %eax")
            else:
                if dtype == "float":
                    self.output.append(f"    movss -{offset}(%ebp), %xmm0")
                else:
                    self.output.append(f"    movl -{offset}(%ebp), %eax")

        elif etype == 'BinaryExpression':
            op = expr['operator']
            ltype = expr['left'].get('resolved_type')
            rtype = expr['right'].get('resolved_type')
            is_float = ltype == 'float' or rtype == 'float'

            if is_float:
                self.gen_expression(expr['right'])
                self.output.append("    sub $4, %esp")
                self.output.append("    movss %xmm0, (%esp)")
                self.gen_expression(expr['left'])
                self.output.append("    movss (%esp), %xmm1")
                self.output.append("    add $4, %esp")

                if op == '+':
                    self.output.append("    addss %xmm1, %xmm0")
                elif op == '-':
                    self.output.append("    subss %xmm1, %xmm0")
                elif op == '*':
                    self.output.append("    mulss %xmm1, %xmm0")
                elif op == '/':
                    self.output.append("    divss %xmm1, %xmm0")
                else:
                    self.output.append(f"    # Operador {op} não suportado para float")
            else:
                self.gen_expression(expr['right'])
                self.output.append("    push %eax")
                self.gen_expression(expr['left'])
                self.output.append("    pop %ebx")

                if op == '+':
                    self.output.append("    addl %ebx, %eax")
                elif op == '-':
                    self.output.append("    subl %ebx, %eax")
                elif op == '*':
                    self.output.append("    imull %ebx, %eax")
                elif op == '/':
                    self.output.append("    cltd")
                    self.output.append("    idivl %ebx")
                elif op in ('>=', '<=', '>', '<'):
                    self.output.append("    cmpl %ebx, %eax")
                    label_true = self.new_label()
                    label_end = self.new_label()
                    jmp_instr = {
                        '>=': 'jl',
                        '<=': 'jg',
                        '>': 'jle',
                        '<': 'jge',
                    }[op]
                    self.output.append(f"    {jmp_instr} {label_true}")
                    self.output.append("    movl $1, %eax")
                    self.output.append(f"    jmp {label_end}")
                    self.output.append(f"{label_true}:")
                    self.output.append("    movl $0, %eax")
                    self.output.append(f"{label_end}:")
                else:
                    self.output.append(f"    # Operador {op} não suportado, movl $0, %eax")
                    self.output.append("    movl $0, %eax")

        else:
            self.output.append(f"    # Expressão tipo {etype} não suportada")

    def new_label(self):
        self._label_count += 1
        return f".L{self._label_count}"
