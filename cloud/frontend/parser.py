class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class ASTNode:
    pass

class ExpressionNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"ExpressionNode({self.left}, {self.operator}, {self.right})"

class IfNode(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f"IfNode({self.condition}, {self.body}, {self.else_body})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()
    
    def next_token(self):
        self.current_token = self.tokens.pop(0) if self.tokens else Token('EOF', None)
    
    def parse(self):
        if self.current_token.type == 'if':
            return self.parse_if()
        else:
            raise SyntaxError(f'Unexpected token: {self.current_token}')
    
    def parse_if(self):
        self.next_token()  # 'if' token'ını atla
        condition = self.parse_expression()
        body = self.parse_block()
        else_body = None
        
        if self.current_token.type == 'else':
            self.next_token()  # 'else' token'ını atla
            else_body = self.parse_block()
        
        return IfNode(condition, body, else_body)
    
    def parse_expression(self):
        left = self.current_token
        self.next_token()
        operator = self.current_token
        self.next_token()
        right = self.current_token
        self.next_token()
        
        return ExpressionNode(left, operator, right)
    
    def parse_block(self):
        statements = []
        while self.current_token.type not in {'else', 'EOF'}:
            if self.current_token.type == 'NEWLINE':
                self.next_token()
                continue
            statements.append(self.current_token)
            self.next_token()
        return statements

# Örnek kullanım
tokens = [
    Token('if', 'if'), Token('IDENTIFIER', 'x'), Token('OPERATOR', '=='), Token('NUMBER', 5),
    Token('NEWLINE', '\n'), Token('IDENTIFIER', 'print'), Token('STRING', '"x is 5"'),
    Token('NEWLINE', '\n'), Token('else', 'else'), Token('NEWLINE', '\n'),
    Token('IDENTIFIER', 'print'), Token('STRING', '"x is not 5"'), Token('EOF', None)
]
parser = Parser(tokens)
ast = parser.parse()
print(ast)
