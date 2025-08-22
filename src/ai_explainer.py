"""
AI-powered educational explanations for detected bugs and code issues.
Currently uses mock responses for demonstration - real AI integration coming soon.
"""
import json
from typing import Dict, Any, List, Optional

class AIExplainer:
    """
    Generates educational explanations for code issues detected by static/dynamic analysis.
    
    Currently provides mock explanations for demonstration purposes.
    Future versions will integrate with OpenAI/Anthropic APIs.
    """
    
    def __init__(self, api_key: Optional[str] = None, mock_mode: bool = True):
        """
        Initialize the AI explainer.
        
        Args:
            api_key: OpenAI/Anthropic API key (for future real integration)
            mock_mode: If True, uses educational mock responses for demo
        """
        self.api_key = api_key
        self.mock_mode = mock_mode or api_key is None
        
        if not self.mock_mode:
            # Future: Initialize real AI client
            # self.client = openai.OpenAI(api_key=api_key)
            print("🔄 Real AI integration - coming soon!")
    
    def explain_analysis_results(self, static_results: Dict[str, Any], 
                               dynamic_results: Optional[Any] = None,
                               code: str = "") -> Dict[str, Any]:
        """
        Generate educational explanation for analysis results.
        
        Args:
            static_results: Results from static analysis (dict)
            dynamic_results: Results from dynamic execution (ExecutionResult or dict)
            code: Original code being analyzed
            
        Returns:
            Dictionary with explanations, learning tips, and suggested fixes
        """
        
        # Convert ExecutionResult dataclass to dict if needed
        if dynamic_results and hasattr(dynamic_results, '__dataclass_fields__'):
            # Convert dataclass to dict
            dynamic_dict = {
                'success': dynamic_results.success,
                'error_type': dynamic_results.error_type,
                'error_message': dynamic_results.error_message,
                'execution_time': dynamic_results.execution_time,
                'output': dynamic_results.output,
                'traceback_info': dynamic_results.traceback_info
            }
            dynamic_results = dynamic_dict
        
        # Handle syntax errors first
        if not static_results.get('syntax_valid', True):
            return self._explain_syntax_error(static_results['syntax_error'])
        
        # Handle runtime errors
        if dynamic_results and not dynamic_results.get('success', True):
            return self._explain_runtime_error(dynamic_results, static_results)
        
        # Handle static analysis issues
        if static_results.get('issues'):
            return self._explain_static_issues(static_results['issues'], static_results)
        
        # No major issues found
        return self._generate_positive_feedback(static_results)
    
    def _explain_syntax_error(self, syntax_error: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explanation for syntax errors"""
        
        error_msg = syntax_error.get('message', '').lower()
        line = syntax_error.get('line', 0)
        
        # Pattern-based explanations for common syntax errors
        if 'invalid syntax' in error_msg:
            explanation = self._get_invalid_syntax_explanation()
        elif 'unexpected eof' in error_msg:
            explanation = self._get_unexpected_eof_explanation()
        elif 'indentation' in error_msg or 'expected an indented block' in error_msg:
            explanation = self._get_indentation_explanation()
        elif 'missing parentheses' in error_msg:
            explanation = self._get_missing_parentheses_explanation()
        else:
            explanation = self._get_generic_syntax_explanation(error_msg)
        
        explanation['error_location'] = f"Line {line}"
        explanation['original_error'] = syntax_error.get('message', '')
        
        return explanation
    
    def _explain_runtime_error(self, dynamic_results: Dict[str, Any], 
                             static_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explanation for runtime errors"""
        
        error_type = dynamic_results.get('error_type', '')
        error_msg = dynamic_results.get('error_message', '')
        
        if error_type == 'IndexError':
            return self._get_index_error_explanation(dynamic_results, static_results)
        elif error_type == 'TypeError':
            return self._get_type_error_explanation(dynamic_results)
        elif error_type == 'NameError':
            return self._get_name_error_explanation(dynamic_results)
        elif error_type == 'ValueError':
            return self._get_value_error_explanation(dynamic_results)
        elif error_type == 'ZeroDivisionError':
            return self._get_zero_division_explanation(dynamic_results)
        else:
            return self._get_generic_runtime_explanation(error_type, error_msg)
    
    def _explain_static_issues(self, issues: List[Dict[str, Any]], 
                             static_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explanation for static analysis issues"""
        
        # Find the highest severity issue to focus on
        severity_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        primary_issue = max(issues, key=lambda x: severity_order.get(x.get('severity', 'low'), 0))
        
        issue_type = primary_issue.get('type', '')
        
        if issue_type == 'potential_index_error':
            return self._get_potential_index_error_explanation(primary_issue, issues)
        elif issue_type == 'eval_usage':
            return self._get_security_risk_explanation(primary_issue)
        elif issue_type == 'bare_except':
            return self._get_exception_handling_explanation(primary_issue)
        elif issue_type == 'long_function':
            return self._get_complexity_explanation(primary_issue, static_results)
        elif issue_type == 'missing_docstring':
            return self._get_documentation_explanation(primary_issue, issues)
        else:
            return self._get_code_quality_explanation(primary_issue, issues)
    
    # Specific explanation generators
    
    def _get_invalid_syntax_explanation(self) -> Dict[str, Any]:
        return {
            'category': 'syntax_error',
            'title': 'Invalid Syntax Detected',
            'simple_explanation': 'Python couldn\'t understand the structure of your code.',
            'detailed_explanation': (
                'Syntax errors occur when Python can\'t parse your code according to its grammar rules. '
                'This usually means there\'s a typo, missing punctuation, or incorrect code structure. '
                'Common causes include missing colons after if/for/def statements, unmatched parentheses '
                'or brackets, incorrect indentation, or typos in keywords.'
            ),
            'learning_focus': 'Python syntax rules and code structure',
            'common_causes': [
                'Missing colon (:) after if, for, def, class statements',
                'Unmatched parentheses, brackets, or quotes',
                'Incorrect indentation (mixing tabs and spaces)',
                'Typos in Python keywords (eg: "fro" instead of "for")',
                'Invalid variable names (starting with numbers or using reserved words)'
            ],
            'fix_strategy': (
                '1. Check the line number in the error message\n'
                '2. Look for missing colons, unmatched brackets, or indentation issues\n'
                '3. Use an IDE with syntax highlighting to spot errors easily\n'
                '4. Read the error message carefully - it often hints at the problem\n'
                '5. Check for typos in keywords and variable names'
            ),
            'learning_tip': '💡 Use an IDE like VS Code or PyCharm with Python syntax highlighting to catch these errors as you type!',
            'prevention_tip': '🛡️ Enable auto-formatting in your editor to catch indentation and spacing issues automatically.'
        }
    
    def _get_index_error_explanation(self, dynamic_results: Dict[str, Any], 
                                   static_results: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'category': 'runtime_error',
            'title': 'List Index Out of Range',
            'simple_explanation': 'Your code tried to access a list element that doesn\'t exist.',
            'detailed_explanation': (
                'IndexError happens when you try to access a list element using an index that\'s too large. '
                'Python lists use 0-based indexing, so a list of length 3 has valid indices 0, 1, 2. '
                'Trying to access index 3 or higher will cause this error. This is often caused by '
                'off-by-one errors in loops, especially when using range(len(list) + 1) instead of range(len(list)). '
                'It\'s one of the most common beginner mistakes in Python.'
            ),
            'learning_focus': 'List indexing, loop boundaries, and the range() function',
            'what_happened': (
                f"Your code encountered: {dynamic_results.get('error_message', 'IndexError')}\n"
                f"This means you tried to access an index that doesn't exist in your list."
            ),
            'common_causes': [
                'Using range(len(list) + 1) instead of range(len(list))',
                'Hardcoding loop ranges instead of using len()',
                'Not accounting for empty lists',
                'Using len(list) as an index (it\'s always one too many!)',
                'Confusion between list length and maximum valid index'
            ],
            'fix_strategy': (
                '1. Use range(len(your_list)) for safe iteration\n'
                '2. Check if the list is empty before accessing elements\n'
                '3. Remember: if len(list) = 3, valid indices are 0, 1, 2\n'
                '4. Consider using "for item in list:" instead of index-based loops\n'
                '5. Use enumerate() if you need both index and value: "for i, item in enumerate(list):"'
            ),
            'prevention_tip': '🛡️ Use "for item in my_list:" when you don\'t need indices, or enumerate() when you do.',
            'learning_tip': '💡 Remember: Python lists are 0-indexed. A list of length N has indices 0 through N-1!',
            'debug_tip': '🔍 Print the list length and the index you\'re trying to access to debug range issues.'
        }
    
    def _get_potential_index_error_explanation(self, issue: Dict[str, Any], 
                                             all_issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            'category': 'static_analysis_warning',
            'title': 'Potential Index Error Detected',
            'simple_explanation': 'Your loop might try to access list elements that don\'t exist.',
            'detailed_explanation': (
                f'Static analysis found a potential IndexError pattern on line {issue.get("line", 0)}. '
                'The pattern range(len(list) + N) is dangerous because it creates indices that exceed '
                'the list boundaries. This is a very common beginner mistake that will cause your '
                'program to crash when it runs. Even though your code looks correct at first glance, '
                'this off-by-one error will definitely cause problems.'
            ),
            'learning_focus': 'Preventing runtime errors through careful loop design',
            'risk_level': 'High - will likely cause runtime crash',
            'pattern_detected': issue.get('pattern', 'Risky loop pattern'),
            'fix_strategy': (
                '1. Change range(len(items) + 1) to range(len(items))\n'
                '2. Or use: for item in items: instead of index-based loops\n'
                '3. If you need indices: for i, item in enumerate(items):\n'
                '4. Always test with different list sizes, including empty lists\n'
                '5. Use len(items) - 1 as the maximum index, not len(items)'
            ),
            'why_dangerous': (
                'If your list has 3 items, len(items) = 3, so range(len(items) + 1) creates [0,1,2,3]. '
                'But items[3] doesn\'t exist! Valid indices are only 0, 1, 2. The +1 creates an index '
                'that will always be out of bounds.'
            ),
            'learning_tip': '💡 When in doubt, use "for item in my_list:" - it\'s safer and more readable!',
            'prevention_tip': '🛡️ Always test your loops with lists of different sizes, including empty ones.'
        }
    
    def _get_security_risk_explanation(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'category': 'security_warning',
            'title': 'Security Risk: eval() Usage Detected',
            'simple_explanation': 'Using eval() can execute malicious code and is a serious security vulnerability.',
            'detailed_explanation': (
                f'eval() usage detected on line {issue.get("line", 0)}. The eval() function executes '
                'any Python code passed to it as a string, which makes it extremely dangerous. '
                'If an attacker can control the input to eval(), they can run any code they want '
                'on your system - delete files, steal data, or install malware. This is why eval() '
                'is considered one of the most dangerous functions in Python.'
            ),
            'learning_focus': 'Secure coding practices and safer alternatives to eval()',
            'risk_level': 'Critical - potential security vulnerability',
            'why_dangerous': [
                'Can execute arbitrary malicious code',
                'Allows access to system functions and files',
                'Difficult to sanitize input safely',
                'Opens door to code injection attacks',
                'Can bypass security restrictions'
            ],
            'safer_alternatives': [
                'ast.literal_eval() for safe evaluation of literals',
                'json.loads() for parsing JSON data',
                'Custom parsing functions for specific formats',
                'Validation and whitelisting for user input',
                'Use dictionaries or if-elif chains instead of dynamic execution'
            ],
            'fix_strategy': (
                '1. Replace eval() with ast.literal_eval() if you need to parse literals\n'
                '2. Use json.loads() for JSON data\n'
                '3. Write custom validation for user input\n'
                '4. Never use eval() with untrusted input\n'
                '5. Consider if you really need dynamic code execution'
            ),
            'learning_tip': '🚨 Security rule: Never use eval() with user input. There\'s almost always a safer alternative!',
            'prevention_tip': '🛡️ If you think you need eval(), step back and find a safer approach. Your future self will thank you.'
        }
    
    def _generate_positive_feedback(self, static_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate encouraging feedback when no major issues are found"""
        
        metrics = static_results.get('metrics', {})
        functions = static_results.get('functions', [])
        
        return {
            'category': 'code_review',
            'title': 'Code Analysis Complete - Looking Good!',
            'simple_explanation': 'No major issues detected in your code.',
            'detailed_feedback': (
                f'Your code passed static analysis successfully! '
                f'Found {metrics.get("function_count", 0)} functions across '
                f'{metrics.get("total_lines", 0)} lines. The code appears to follow '
                f'good Python practices and doesn\'t contain obvious bug patterns. '
                f'This suggests you\'re developing good coding habits!'
            ),
            'code_metrics': {
                'total_lines': metrics.get('total_lines', 0),
                'functions': len(functions),
                'complexity': 'Appears reasonable',
                'issues_found': len(static_results.get('issues', []))
            },
            'suggestions_for_improvement': [
                'Add docstrings to functions if not already present',
                'Consider adding type hints for better code documentation',
                'Write unit tests to verify behavior with edge cases',
                'Add comments for any complex logic sections',
                'Consider using more descriptive variable names'
            ],
            'next_steps': (
                'Your code structure looks solid! Consider testing it with different inputs '
                'and edge cases to ensure it handles all scenarios correctly. Also think about '
                'error handling for unexpected inputs.'
            ),
            'learning_tip': '✅ Great job! Clean, well-structured code is easier to debug, maintain, and understand.',
            'keep_improving': '📚 Continue learning about advanced Python patterns, testing, and documentation practices!'
        }

    # Additional helper methods for completeness
    
    def _get_type_error_explanation(self, dynamic_results: Dict[str, Any]) -> Dict[str, Any]:
        error_msg = dynamic_results.get('error_message', '').lower()
        
        if 'can only concatenate str' in error_msg:
            focus = 'String concatenation with incompatible types'
            cause = 'Tried to use + operator between string and non-string (like number)'
            fix = 'Convert the number to string: str(number), or use f-strings: f"text {number}"'
        elif 'unsupported operand' in error_msg:
            focus = 'Mathematical operations between incompatible types'
            cause = 'Tried to do math (like +, -, *) between incompatible data types'
            fix = 'Make sure both operands are the same type: convert strings to int/float or vice versa'
        else:
            focus = 'Type compatibility in operations'
            cause = 'Operation attempted between incompatible data types'
            fix = 'Check data types and convert as needed before operations'
        
        return {
            'category': 'runtime_error',
            'title': 'Type Error - Incompatible Operation',
            'simple_explanation': 'You tried to perform an operation between incompatible data types.',
            'detailed_explanation': (
                'TypeError occurs when you try to use an operation or function on data of the wrong type. '
                'For example, you can\'t add a string and a number directly, or multiply strings by strings. '
                'Python is dynamically typed but still enforces type compatibility for operations. '
                'This often happens when working with user input (which is always strings initially).'
            ),
            'learning_focus': focus,
            'what_happened': f"Error: {dynamic_results.get('error_message', 'Type incompatibility detected')}",
            'likely_cause': cause,
            'fix_strategy': (
                f'1. {fix}\n'
                '2. Check data types with type() function\n'
                '3. Use isinstance() to verify types before operations\n'
                '4. Convert types explicitly: int(), float(), str()\n'
                '5. Use f-strings for string formatting with numbers'
            ),
            'learning_tip': '💡 Remember: "123" + 456 won\'t work, but "123" + str(456) or int("123") + 456 will!',
            'prevention_tip': '🛡️ Always validate and convert input data types before using them in operations.'
        }

    def _get_unexpected_eof_explanation(self) -> Dict[str, Any]:
        return {
            'category': 'syntax_error',
            'title': 'Unexpected End of File',
            'simple_explanation': 'Python expected more code but reached the end of your file.',
            'detailed_explanation': (
                'This error occurs when Python is expecting closing brackets, parentheses, quotes, '
                'or more code but reaches the end of the file instead. It\'s like starting a sentence '
                'but never finishing it. Common causes include unclosed strings, missing closing '
                'brackets, or incomplete function definitions.'
            ),
            'fix_strategy': 'Check for unclosed quotes, brackets, parentheses, or incomplete statements.',
            'learning_tip': '💡 Use an IDE that highlights matching brackets to avoid this error!'
        }

    # Placeholder methods for other error types
    def _get_indentation_explanation(self) -> Dict[str, Any]:
        return {'category': 'syntax_error', 'title': 'Indentation Error', 'simple_explanation': 'Python uses indentation to organize code blocks.'}
    
    def _get_missing_parentheses_explanation(self) -> Dict[str, Any]:
        return {'category': 'syntax_error', 'title': 'Missing Parentheses', 'simple_explanation': 'A closing parenthesis is missing.'}
    
    def _get_generic_syntax_explanation(self, error_msg: str) -> Dict[str, Any]:
        return {'category': 'syntax_error', 'title': 'Syntax Error', 'simple_explanation': f'Python found a syntax problem: {error_msg}'}
    
    def _get_name_error_explanation(self, dynamic_results: Dict[str, Any]) -> Dict[str, Any]:
        return {'category': 'runtime_error', 'title': 'Name Error', 'simple_explanation': 'Used a variable that wasn\'t defined.'}
    
    def _get_value_error_explanation(self, dynamic_results: Dict[str, Any]) -> Dict[str, Any]:
        return {'category': 'runtime_error', 'title': 'Value Error', 'simple_explanation': 'Passed incorrect value to a function.'}
    
    def _get_zero_division_explanation(self, dynamic_results: Dict[str, Any]) -> Dict[str, Any]:
        return {'category': 'runtime_error', 'title': 'Zero Division Error', 'simple_explanation': 'Attempted to divide by zero.'}
    
    def _get_generic_runtime_explanation(self, error_type: str, error_msg: str) -> Dict[str, Any]:
        return {'category': 'runtime_error', 'title': f'{error_type}', 'simple_explanation': f'Runtime error: {error_msg}'}
    
    def _get_exception_handling_explanation(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        return {'category': 'code_quality_warning', 'title': 'Poor Exception Handling', 'simple_explanation': 'Bare except clause is too broad.'}
    
    def _get_complexity_explanation(self, issue: Dict[str, Any], static_results: Dict[str, Any]) -> Dict[str, Any]:
        return {'category': 'code_quality_warning', 'title': 'High Complexity', 'simple_explanation': 'Function is too complex.'}
    
    def _get_documentation_explanation(self, issue: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {'category': 'code_quality_warning', 'title': 'Missing Documentation', 'simple_explanation': 'Function lacks docstring.'}
    
    def _get_code_quality_explanation(self, issue: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {'category': 'code_quality_warning', 'title': 'Code Quality Issue', 'simple_explanation': 'General code quality concern.'}


# Test the AI explainer
if __name__ == "__main__":
    print("🤖 AI Explainer Demo")
    print("=" * 40)
    
    explainer = AIExplainer()
    
    # Test 1: Syntax error explanation
    syntax_error_results = {
        'syntax_valid': False,
        'syntax_error': {
            'line': 5,
            'message': 'invalid syntax',
            'text': 'if age >= 18'
        }
    }
    
    print("🔴 Syntax Error Example:")
    explanation1 = explainer.explain_analysis_results(syntax_error_results)
    print(f"Title: {explanation1['title']}")
    print(f"Simple: {explanation1['simple_explanation']}")
    print(f"Tip: {explanation1['learning_tip']}")
    
    print("\n" + "-" * 30)
    
    # Test 2: Static analysis issue
    static_issue_results = {
        'syntax_valid': True,
        'issues': [{
            'type': 'potential_index_error',
            'severity': 'high',
            'line': 10,
            'message': 'Loop range may exceed list bounds',
            'pattern': 'range(len(list) + 1)'
        }],
        'metrics': {'function_count': 1, 'total_lines': 15}
    }
    
    print("🟠 Static Analysis Issue Example:")
    explanation2 = explainer.explain_analysis_results(static_issue_results)
    print(f"Title: {explanation2['title']}")
    print(f"Simple: {explanation2['simple_explanation']}")
    print(f"Risk: {explanation2['risk_level']}")
    
    print("\n" + "-" * 30)
    
    # Test 3: No issues found
    clean_results = {
        'syntax_valid': True,
        'issues': [],
        'metrics': {'function_count': 2, 'total_lines': 20},
        'functions': [{'name': 'test1'}, {'name': 'test2'}]
    }
    
    print("✅ Clean Code Example:")
    explanation3 = explainer.explain_analysis_results(clean_results)
    print(f"Title: {explanation3['title']}")
    print(f"Simple: {explanation3['simple_explanation']}")
    print(f"Tip: {explanation3['learning_tip']}")
