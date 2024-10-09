# Prueba de Interprete simple

import re

# Lexer: Análisis léxico
TOKEN_REGEX = re.compile(r"\s*(?:(\d+)|(.))")

def tokenize(code):
    """Convertir el código en una lista de tokens (números y operadores)."""
    tokens = []
    for number, operator in TOKEN_REGEX.findall(code): 
        if number:
            tokens.append(('NUMBER', int(number)))
        elif operator in '+-*/()':
            tokens.append((operator, operator))
        else:
            raise SyntaxError(f"Carácter no esperado: {operator}")
    return tokens

# Parser: Análisis sintáctico
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        """Mirar el siguiente token sin consumirlo."""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type):
        """Consumir un token si coincide con el tipo esperado."""
        token = self.peek()
        if token is None or token[0] != expected_type:
            raise SyntaxError(f"Se esperaba {expected_type}, pero se encontró {token}")
        self.pos += 1
        return token

    def parse_expression(self):
        """Parsear una expresión completa."""
        return self.parse_term()

    def parse_term(self):
        """Parsear términos que pueden incluir suma y resta."""
        node = self.parse_factor()
        while self.peek() and self.peek()[0] in ('+', '-'):
            operator = self.consume(self.peek()[0])[0]
            right_node = self.parse_factor()
            node = (operator, node, right_node)
        return node

    def parse_factor(self):
        """Parsear factores que pueden incluir multiplicación y división."""
        node = self.parse_primary()
        while self.peek() and self.peek()[0] in ('*', '/'):
            operator = self.consume(self.peek()[0])[0]
            right_node = self.parse_primary()
            node = (operator, node, right_node)
        return node

    def parse_primary(self):
        """Parsear valores primarios como números o expresiones entre paréntesis."""
        token = self.peek()
        if token[0] == 'NUMBER':
            return self.consume('NUMBER')[1]
        elif token[0] == '(':
            self.consume('(')
            node = self.parse_expression()
            self.consume(')')
            return node
        else:
            raise SyntaxError(f"Se esperaba un número o un '(', pero se encontró {token}")

# Evaluador
def evaluate(node):
    """Evaluar el árbol sintáctico generado por el parser."""
    if isinstance(node, int):
        return node
    operator, left, right = node
    if operator == '+':
        return evaluate(left) + evaluate(right)
    elif operator == '-':
        return evaluate(left) - evaluate(right)
    elif operator == '*':
        return evaluate(left) * evaluate(right)
    elif operator == '/':
        return evaluate(left) / evaluate(right)
    else:
        raise SyntaxError(f"Operador no reconocido: {operator}")

# Intérprete: juntar todo
def interpret(code):
    tokens = tokenize(code)
    parser = Parser(tokens)
    tree = parser.parse_expression()
    return evaluate(tree)

# Ejemplo de uso
while True:
    try:
        code = input(">>> ")
        if code.strip() == "exit":
            break
        result = interpret(code)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
