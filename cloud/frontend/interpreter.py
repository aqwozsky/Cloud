import os
import sys

class RuntimeError(Exception):
    pass

class Runtime:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        if name not in self.variables:
            raise RuntimeError(f"Undefined variable: {name}")
        return self.variables[name]

    def set_function(self, name, params, body):
        self.functions[name] = (params, body)

    def get_function(self, name):
        if name not in self.functions:
            raise RuntimeError(f"Undefined function: {name}")
        return self.functions[name]

class Interpreter:
    def __init__(self, ast, runtime=None):
        self.ast = ast
        self.runtime = runtime or Runtime()

    def interpret(self):
        self.visit(self.ast)

    def visit(self, node):
        method_name = f'visit_{node.__class__.__name__.lower()}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise RuntimeError(f'No visit_{node.__class__.__name__.lower()} method')

    def visit_program(self, node):
        for child in node.value:
            self.visit(child)

    def visit_print(self, node):
        value = self.visit(node.value)
        print(value)

    def visit_assignment(self, node):
        var_name, expr_node = node.value
        value = self.visit(expr_node)
        self.runtime.set_variable(var_name, value)

    def visit_if(self, node):
        condition, true_block = node.condition, node.body
        if self.visit(condition):
            self.visit(true_block)
        elif node.else_body:
            self.visit(node.else_body)

    def visit_while(self, node):
        condition, body = node.condition, node.body
        while self.visit(condition):
            self.visit(body)

    def visit_function_def(self, node):
        func_name, params, body = node.name, node.params, node.body
        self.runtime.set_function(func_name, params, body)

    def visit_call(self, node):
        func_name, args = node.name, node.args
        func = self.runtime.get_function(func_name)
        params, body = func

        if len(params) != len(args):
            raise RuntimeError(f'Argument count mismatch in call to {func_name}')

        local_runtime = Runtime()
        for param, arg in zip(params, args):
            local_runtime.set_variable(param, self.visit(arg))

        prev_runtime = self.runtime
        self.runtime = local_runtime
        try:
            self.visit(body)
        finally:
            self.runtime = prev_runtime

    def visit_import(self, node):
        module_name = node.value.strip('"\'')
        module_path = f"{module_name}.cl"

        if not os.path.isfile(module_path):
            raise RuntimeError(f'Module {module_name} not found')

        with open(module_path, 'r') as f:
            source_code = f.read()
        
        # Tokenize and parse the module
        from lexer import tokenize
        from parser import Parser
        
        tokens = tokenize(source_code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Create a local interpreter for the module
        local_interpreter = Interpreter(ast, self.runtime)
        local_interpreter.interpret()

    def visit_block(self, node):
        for statement in node.value:
            self.visit(statement)

    def visit_number(self, node):
        return node.value

    def visit_string(self, node):
        return node.value

    def visit_identifier(self, node):
        return self.runtime.get_variable(node.value)

    def visit_binary_op(self, node):
        op, left_node, right_node = node.operator, node.left, node.right
        left_value = self.visit(left_node)
        right_value = self.visit(right_node)

        if op == '+':
            return left_value + right_value
        elif op == '-':
            return left_value - right_value
        elif op == '*':
            return left_value * right_value
        elif op == '/':
            return left_value / right_value
        elif op == '<':
            return left_value < right_value
        elif op == '>':
            return left_value > right_value
        elif op == '==':
            return left_value == right_value
        else:
            raise RuntimeError(f'Unknown operator: {op}')
