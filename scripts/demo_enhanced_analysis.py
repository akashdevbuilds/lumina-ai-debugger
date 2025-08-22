#!/usr/bin/env python3
"""
Demo script showcasing the enhanced static analysis capabilities
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.static_analysis import enhanced_analyze_code
import json

def demo_enhanced_analysis():
    """Demonstrate the enhanced static analysis on various code samples"""
    
    print("🔍 Enhanced Static Analysis Demo")
    print("=" * 50)
    
    # Sample 1: Clean code
    clean_code = '''
def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number using iteration."""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
'''
    
    # Sample 2: Buggy code with multiple issues
    buggy_code = '''
def process_data(data_list):
    results = []
    for i in range(len(data_list) + 1):  # IndexError waiting to happen!
        try:
            # Security risk using eval
            result = eval(f"data_list[{i}] * 2")
            results.append(result)
            print()  # Empty print - debug leftover?
        except:  # Bare except - too broad!
            pass
    
    unused_var = "I'm never used"
    return results

def another_func():  # Missing docstring
    x = 5
    return x
'''
    
    # Sample 3: Complex function
    complex_code = '''
def complex_algorithm(data, threshold=10):
    """A complex algorithm with high cyclomatic complexity."""
    result = []
    for item in data:
        if item > threshold:
            if isinstance(item, int):
                if item % 2 == 0:
                    if item > 100:
                        result.append(item * 3)
                    elif item > 50:
                        result.append(item * 2)
                    else:
                        result.append(item)
                else:
                    if item > 75:
                        result.append(item + 10)
                    else:
                        result.append(item + 5)
            else:
                result.append(float(item))
        elif item < 0:
            result.append(0)
        else:
            result.append(item)
    return result
'''
    
    samples = [
        ("Clean Code", clean_code),
        ("Buggy Code", buggy_code), 
        ("Complex Code", complex_code)
    ]
    
    for name, code in samples:
        print(f"\n📝 Analyzing: {name}")
        print("-" * 30)
        
        analysis = enhanced_analyze_code(code)
        
        # Display summary
        print(f"✅ Syntax Valid: {analysis['syntax_valid']}")
        print(f"📊 Issues Found: {len(analysis['issues'])}")
        print(f"🏗️  Functions: {len(analysis['functions'])}")
        print(f"📏 Total Lines: {analysis['metrics']['total_lines']}")
        
        # Display issues
        if analysis['issues']:
            print("\n🚨 Issues Detected:")
            severity_icons = {
                'low': '🟡', 'medium': '🟠', 
                'high': '🔴', 'critical': '💀'
            }
            for issue in analysis['issues']:
                icon = severity_icons.get(issue['severity'], '⚪')
                print(f"  {icon} Line {issue['line']}: {issue['message']}")
        
        # Display complexity
        if analysis['complexity']:
            print("\n⚡ Complexity Analysis:")
            risk_icons = {
                'low': '🟢', 'moderate': '🟡', 
                'high': '🔴', 'very_high': '💀'
            }
            for func in analysis['complexity']:
                icon = risk_icons.get(func['classification'], '⚪')
                print(f"  {icon} {func['name']}: {func['complexity']} ({func['classification']})")
        
        # Display metrics
        metrics = analysis['metrics']
        print(f"\n📈 Code Metrics:")
        print(f"  • Total lines: {metrics['total_lines']}")
        print(f"  • Non-empty lines: {metrics['non_empty_lines']}")
        print(f"  • Comment lines: {metrics['comment_lines']}")
        print(f"  • Functions: {metrics['function_count']}")
        
        # Display variable analysis
        vars_info = analysis['variables']
        if vars_info['potentially_unused']:
            print(f"\n🔍 Potentially unused variables: {', '.join(vars_info['potentially_unused'])}")

def demo_json_output():
    """Show how to get detailed JSON output for tool integration"""
    print("\n\n🔧 JSON Output for Tool Integration")
    print("=" * 40)
    
    sample_code = '''
def divide(a, b):
    try:
        result = eval(f"{a} / {b}")  # Security issue
        print()  # Debug leftover
        return result
    except:  # Too broad
        return None
'''
    
    analysis = enhanced_analyze_code(sample_code)
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    demo_enhanced_analysis()
    demo_json_output()
