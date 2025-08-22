import ast
import logging
from typing import List, Dict, Any
from radon.complexity import cc_visit

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class BugPatternDetector(ast.NodeVisitor):
    """Advanced AST visitor that detects multiple bug patterns"""
    
    def __init__(self):
        self.issues = []
        self.functions = []
        self.variables_used = set()
        self.variables_defined = set()
    
    def visit_For(self, node):
        """Detect potential IndexError patterns"""
        # Check for range(len(list) + 1) pattern
        if (isinstance(node.iter, ast.Call) and 
            isinstance(node.iter.func, ast.Name) and 
            node.iter.func.id == 'range'):
            
            if (len(node.iter.args) == 1 and
                isinstance(node.iter.args[0], ast.BinOp) and
                isinstance(node.iter.args[0].op, ast.Add)):
                
                self.issues.append({
                    'type': 'potential_index_error',
                    'severity': 'high',
                    'line': node.lineno,
                    'message': 'Loop range may exceed list bounds, potential IndexError',
                    'pattern': 'range(len(list) + N)'
                })
        
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        """Analyze function definitions"""
        # Store function info
        func_info = {
            'name': node.name,
            'line': node.lineno,
            'args': len(node.args.args),
            'has_docstring': ast.get_docstring(node) is not None
        }
        self.functions.append(func_info)
        
        # Check for missing docstrings
        if not func_info['has_docstring']:
            self.issues.append({
                'type': 'missing_docstring',
                'severity': 'medium',
                'line': node.lineno,
                'message': f'Function "{node.name}" lacks documentation',
                'pattern': 'undocumented_function'
            })
        
        # Check for overly long functions (>30 lines as threshold)
        if hasattr(node, 'end_lineno'):
            func_length = node.end_lineno - node.lineno
            if func_length > 30:
                self.issues.append({
                    'type': 'long_function',
                    'severity': 'medium',
                    'line': node.lineno,
                    'message': f'Function "{node.name}" is {func_length} lines (consider breaking down)',
                    'pattern': 'long_function'
                })
        
        self.generic_visit(node)
    
    def visit_Name(self, node):
        """Track variable usage patterns"""
        if isinstance(node.ctx, ast.Store):
            self.variables_defined.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.variables_used.add(node.id)
        
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """Detect problematic function calls"""
        if isinstance(node.func, ast.Name):
            # Detect print() without debugging context
            if node.func.id == 'print' and len(node.args) == 0:
                self.issues.append({
                    'type': 'empty_print',
                    'severity': 'low',
                    'line': node.lineno,
                    'message': 'Empty print() statement - debugging leftover?',
                    'pattern': 'debug_artifact'
                })
            
            # Detect eval() usage (security risk)
            elif node.func.id == 'eval':
                self.issues.append({
                    'type': 'eval_usage',
                    'severity': 'critical',
                    'line': node.lineno,
                    'message': 'eval() usage detected - security risk!',
                    'pattern': 'security_risk'
                })
        
        self.generic_visit(node)
    
    def visit_Try(self, node):
        """Analyze exception handling patterns"""
        # Check for bare except clauses
        for handler in node.handlers:
            if handler.type is None:
                self.issues.append({
                    'type': 'bare_except',
                    'severity': 'medium',
                    'line': handler.lineno,
                    'message': 'Bare except clause catches all exceptions - too broad',
                    'pattern': 'poor_exception_handling'
                })
        
        self.generic_visit(node)

def enhanced_analyze_code(code_str: str) -> Dict[str, Any]:
    """
    Perform comprehensive static analysis on Python code
    
    Returns detailed analysis including syntax validation, bug patterns,
    complexity metrics, and function information.
    """
    try:
        # Parse the code into AST
        tree = ast.parse(code_str)
        
        # Initialize detector and analyze
        detector = BugPatternDetector()
        detector.visit(tree)
        
        # Get complexity analysis using Radon
        try:
            complexity_blocks = cc_visit(code_str)
            complexity_info = [{
                'name': block.name,
                'complexity': block.complexity,
                'classification': _classify_complexity(block.complexity)
            } for block in complexity_blocks]
        except Exception as e:
            complexity_info = []
            logging.warning(f"Complexity analysis failed: {e}")
        
        # Calculate code metrics
        lines = code_str.split('\n')
        metrics = {
            'total_lines': len(lines),
            'non_empty_lines': len([line for line in lines if line.strip()]),
            'comment_lines': len([line for line in lines if line.strip().startswith('#')]),
            'function_count': len(detector.functions),
            'issues_found': len(detector.issues)
        }
        
        return {
            'syntax_valid': True,
            'issues': detector.issues,
            'functions': detector.functions,
            'complexity': complexity_info,
            'metrics': metrics,
            'variables': {
                'defined': list(detector.variables_defined),
                'used': list(detector.variables_used),
                'potentially_unused': list(detector.variables_defined - detector.variables_used)
            }
        }
        
    except SyntaxError as e:
        return {
            'syntax_valid': False,
            'syntax_error': {
                'line': e.lineno,
                'column': e.offset,
                'message': e.msg,
                'text': e.text.strip() if e.text else None,
                'error_type': 'SyntaxError'
            },
            'issues': [],
            'functions': [],
            'complexity': [],
            'metrics': {'total_lines': len(code_str.split('\n'))}
        }

def _classify_complexity(complexity: int) -> str:
    """Classify cyclomatic complexity into risk levels"""
    if complexity <= 10:
        return "low"
    elif complexity <= 20:
        return "moderate"
    elif complexity <= 50:
        return "high"
    else:
        return "very_high"

# Keep backward compatibility with existing functions
def analyse_code(code_str):
    """Legacy function - kept for backward compatibility"""
    analysis = enhanced_analyze_code(code_str)
    for func in analysis.get('functions', []):
        logging.info(f"Function found: {func['name']}")

def analyze_complexity(code_str):
    """Legacy function - kept for backward compatibility"""
    try:
        blocks = cc_visit(code_str)
        for block in blocks:
            logging.info(f"Complexity: {block.name} -> {block.complexity}")
    except Exception as e:
        logging.warning(f"Complexity analysis failed: {e}")

def detect_long_functions(tree, max_lines=50):
    """Legacy function - kept for backward compatibility"""
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno
            end = max(getattr(child, 'lineno', start) for child in ast.walk(node))
            length = end - start + 1
            if length > max_lines:
                logging.warning(f"Long function '{node.name}' ({length} lines)")

def analyze_code(code_str):
    """Legacy function - kept for backward compatibility"""
    tree = ast.parse(code_str)
    analyze_complexity(code_str)
    detect_long_functions(tree)
    # Existing function definition logging
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            logging.info(f"Function found: {node.name}")

# Test the enhanced analyzer
if __name__ == "__main__":
    sample_buggy_code = '''
def process_items(items):
    # This function has multiple issues
    for i in range(len(items) + 1):  # Bug: IndexError waiting to happen
        print(items[i])
        if items[i] > 0:
            try:
                result = eval(f"items[{i}] * 2")  # Security issue!
                print()  # Empty print - debug artifact?
            except:  # Bare except - too broad!
                pass

def another_function():  # Missing docstring
    x = 5
    y = 10
    # y is defined but never used
    return x

# Test with problematic input
try:
    process_items([1, 2, 3])
except Exception as e:
    print(f"Error: {e}")
'''
    
    print("🔍 Enhanced Static Analysis Demo")
    print("=" * 50)
    
    analysis = enhanced_analyze_code(sample_buggy_code)
    
    print(f"Syntax Valid: {'✅' if analysis['syntax_valid'] else '❌'}")
    print(f"Issues Found: {len(analysis.get('issues', []))}")
    print(f"Functions: {len(analysis.get('functions', []))}")
    print(f"Total Lines: {analysis.get('metrics', {}).get('total_lines', 0)}")
    
    print("\n📋 Issues Detected:")
    for issue in analysis.get('issues', []):
        severity_emoji = {'low': '🟡', 'medium': '🟠', 'high': '🔴', 'critical': '💀'}
        print(f"  {severity_emoji.get(issue['severity'], '⚪')} Line {issue['line']}: {issue['message']}")
    
    print("\n📊 Complexity Analysis:")
    for func in analysis.get('complexity', []):
        risk_emoji = {'low': '🟢', 'moderate': '🟡', 'high': '🔴', 'very_high': '💀'}
        print(f"  {risk_emoji.get(func['classification'], '⚪')} {func['name']}: {func['complexity']} ({func['classification']})")

