import ast
import logging
from random import sample

logging.basicConfig(level=logging.INFO , format='%(levelname)s: %(message)s')

def analyse_code(code_str):
    """
    Parse the given code string and log all function definitions.
    """
    tree = ast.parse(code_str)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            logging.info(f"Function found: {node.name} ")

if __name__ == "__main__":
    sample_code = '''
def add (a, b):
    return a + b
'''
    analyse_code(sample_code)

