#!/usr/bin/env python

import sys
import os

# Set custom directory for __pycache__ files
os.environ['PYTHONPYCACHEPREFIX'] = os.path.join(os.path.dirname(__file__), 'logs')

# Define the frontend directory path
frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')

# Add frontend directory to sys.path
sys.path.append(frontend_dir)

# Import modules from the frontend directory
from interpreter import Interpreter
from lexer import tokenize
from parser import Parser

def main():
    if len(sys.argv) < 2:
        print("Usage: cloud [options] <file>.cl")
        sys.exit(1)

    args = sys.argv[1:]

    if args[0] == "--run":
        if len(args) < 2:
            print("Error: No file provided.")
            sys.exit(1)
        file_path = args[1]
        run_file(file_path)
    else:
        print("Unknown option:", args[0])
        sys.exit(1)

def run_file(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    with open(file_path, 'r') as f:
        source_code = f.read()

    tokens = tokenize(source_code)
    parser = Parser(tokens)
    ast = parser.parse()

    # Create an interpreter instance and interpret the AST
    interpreter = Interpreter(ast)
    interpreter.interpret()

def cleanup():
    sys.__doc__.find('')

if __name__ == "__main__":
    main()
