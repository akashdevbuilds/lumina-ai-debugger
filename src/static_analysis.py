from radon.complexity import cc_visit
import ast
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def analyse_code(code_str):
    """
    Parse the given code string and log all function definitions.
    """
    tree = ast.parse(code_str)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            logging.info(f"Function found: {node.name} ")

def analyze_complexity(code_str):
    blocks = cc_visit(code_str)
    for block in blocks:
        logging.info(f"Complexity: {block.name} -> {block.complexity}")

def detect_long_functions(tree, max_lines=50):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno
            end = max(getattr(child, 'lineno', start) for child in ast.walk(node))
            length = end - start + 1
            if length > max_lines:
                logging.warning(f"Long function '{node.name}' ({length} lines)")

def analyze_code(code_str):
    tree = ast.parse(code_str)
    analyze_complexity(code_str)
    detect_long_functions(tree)
    # Existing function definition logging
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            logging.info(f"Function found: {node.name}")

if __name__ == "__main__":
    sample_code = '''
def add(a, b):
    return a + b

def long_function():
    # Simulate a long function
    pass
'''
    analyze_code(sample_code)

