#!/usr/bin/env python3
"""
Integrated Demo: Static Analysis + Dynamic Analysis + AI Explanations

This script demonstrates the full Lumina AI Debugger pipeline:
1. Static analysis to detect potential issues
2. Dynamic analysis to observe runtime behavior  
3. AI explanations to provide educational insights
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.static_analysis import enhanced_analyze_code
from src.dynamic_analysis import run_dynamic_analysis
from src.ai_explainer import AIExplainer
import json


def demo_integrated_analysis():
    """Demonstrate the complete Lumina AI Debugger pipeline"""
    
    print("🌟 LUMINA AI DEBUGGER - INTEGRATED ANALYSIS DEMO")
    print("=" * 60)
    print("📋 Pipeline: Static Analysis → Dynamic Analysis → AI Explanations")
    print()
    
    # Initialize components
    explainer = AIExplainer()
    
    # Test cases that showcase different aspects
    test_cases = [
        {
            'name': 'Clean Code Example',
            'description': 'Well-written code with no issues',
            'code': '''
def calculate_factorial(n):
    """Calculate factorial of n using iteration."""
    if n < 0:
        return None
    elif n <= 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Test the function
print(f"5! = {calculate_factorial(5)}")
print(f"0! = {calculate_factorial(0)}")
'''
        },
        {
            'name': 'Index Error Example',
            'description': 'Code with potential IndexError issue',
            'code': '''
def process_items(items):
    """Process items with a dangerous loop pattern."""
    results = []
    for i in range(len(items) + 1):  # BUG: +1 will cause IndexError
        processed = items[i] * 2
        results.append(processed)
        print(f"Processed item {i}: {processed}")
    return results

# This will crash!
data = [1, 2, 3, 4, 5]
result = process_items(data)
'''
        },
        {
            'name': 'Security Risk Example', 
            'description': 'Code with eval() security vulnerability',
            'code': '''
def calculate_expression(expression):
    """Dangerous: uses eval() which can execute arbitrary code."""
    try:
        result = eval(expression)  # SECURITY RISK!
        return result
    except:  # Bare except - also bad practice
        return "Error in calculation"

# These work but are dangerous
print(calculate_expression("2 + 2"))
print(calculate_expression("10 * 5"))
'''
        },
        {
            'name': 'Type Error Example',
            'description': 'Runtime type error from string/number operations',
            'code': '''
def add_values(a, b):
    """Add two values together."""
    return a + b

# This works
result1 = add_values(10, 20)
print(f"10 + 20 = {result1}")

# This will fail with TypeError
result2 = add_values("10", 20)  # String + int
print(f"'10' + 20 = {result2}")
'''
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔬 TEST CASE {i}: {test_case['name']}")
        print(f"📝 {test_case['description']}")
        print("=" * 60)
        
        code = test_case['code'].strip()
        
        # STEP 1: Static Analysis
        print("\n🔍 STEP 1: Static Analysis")
        print("-" * 30)
        
        static_results = enhanced_analyze_code(code)
        
        print(f"✅ Syntax Valid: {static_results['syntax_valid']}")
        print(f"🚨 Issues Found: {len(static_results.get('issues', []))}")
        print(f"📏 Lines of Code: {static_results['metrics']['total_lines']}")
        print(f"🏗️  Functions: {len(static_results.get('functions', []))}")
        
        if static_results.get('issues'):
            print("\n🚨 Static Analysis Issues:")
            for issue in static_results['issues'][:3]:  # Show top 3
                severity_icon = {'low': '🟡', 'medium': '🟠', 'high': '🔴', 'critical': '💀'}.get(issue['severity'], '⚪')
                print(f"  {severity_icon} Line {issue['line']}: {issue['message']}")
        
        # STEP 2: Dynamic Analysis (with error handling)
        print(f"\n🚀 STEP 2: Dynamic Analysis")
        print("-" * 30)
        
        dynamic_results = run_dynamic_analysis(code, timeout=2.0)
        
        print(f"✅ Execution Success: {dynamic_results.success}")
        print(f"⏱️  Execution Time: {dynamic_results.execution_time:.4f}s")
        print(f"🧠 Memory Usage: {dynamic_results.memory_peak:,} bytes")
        
        if dynamic_results.output:
            print(f"📤 Program Output:")
            output_lines = dynamic_results.output.strip().split('\\n')
            for line in output_lines[:5]:  # Limit output
                print(f"  {line}")
            if len(output_lines) > 5:
                print(f"  ... and {len(output_lines) - 5} more lines")
        
        if not dynamic_results.success:
            print(f"❌ Runtime Error: {dynamic_results.error_type}")
            print(f"💬 Error Message: {dynamic_results.error_message}")
        
        if dynamic_results.performance_metrics:
            metrics = dynamic_results.performance_metrics
            print(f"📊 Execution Metrics:")
            print(f"  • Total events traced: {metrics.get('total_events', 0)}")
            print(f"  • Functions called: {metrics.get('functions_called', 0)}")
            print(f"  • Lines covered: {metrics.get('lines_covered', 0)}")
            print(f"  • Max stack depth: {metrics.get('max_stack_depth', 0)}")
        
        # STEP 3: AI Explanations
        print(f"\n🤖 STEP 3: AI Educational Explanations") 
        print("-" * 30)
        
        # Generate AI explanation based on results
        explanation = explainer.explain_analysis_results(static_results, dynamic_results, code)
        
        print(f"📚 {explanation['title']}")
        print(f"💡 {explanation['simple_explanation']}")
        
        if explanation.get('detailed_explanation'):
            print(f"\\n📖 Detailed Explanation:")
            print(f"   {explanation['detailed_explanation']}")
        
        if explanation.get('learning_tip'):
            print(f"\\n{explanation['learning_tip']}")
            
        if explanation.get('prevention_tip'): 
            print(f"{explanation['prevention_tip']}")
        
        if explanation.get('fix_strategy'):
            print(f"\\n🔧 How to Fix:")
            fix_lines = explanation['fix_strategy'].split('\\n')
            for line in fix_lines[:3]:  # Show first 3 steps
                if line.strip():
                    print(f"   {line.strip()}")
        
        if explanation.get('why_dangerous'):
            print(f"\\n⚠️  Why This Is Dangerous:")
            print(f"   {explanation['why_dangerous']}")
            
        if explanation.get('risk_level'):
            print(f"\\n🎯 Risk Level: {explanation['risk_level']}")
        
        # Show learning focus for educational value
        if explanation.get('learning_focus'):
            print(f"\\n🎓 Learning Focus: {explanation['learning_focus']}")
        
        print("\\n" + "=" * 60)
    
    # Summary
    print(f"\\n🎯 ANALYSIS COMPLETE!")
    print(f"✅ Demonstrated: Static analysis + Dynamic execution + AI explanations")
    print(f"📚 Educational: Each error explained with learning tips and fixes")
    print(f"🛡️  Comprehensive: Covers syntax, runtime, security, and complexity issues")
    print(f"\\n🌟 Lumina AI Debugger helps you understand and fix code issues! 🌟")


def demo_api_usage():
    """Show how to use the components programmatically"""
    print("\\n\\n🔧 API USAGE EXAMPLE")
    print("=" * 40)
    
    # Example of programmatic usage
    code_sample = '''
def risky_function(user_input):
    return eval(user_input)  # Security risk
    
result = risky_function("2 + 2")
'''
    
    print("📝 Code Analysis Pipeline:")
    print("```python")
    print("# 1. Static Analysis")
    print("static_results = enhanced_analyze_code(code)")
    print()
    print("# 2. Dynamic Analysis")  
    print("dynamic_results = run_dynamic_analysis(code)")
    print()
    print("# 3. AI Explanations")
    print("explainer = AIExplainer()")
    print("explanation = explainer.explain_analysis_results(static_results, dynamic_results)")
    print("```")
    
    # Actually run it
    static_results = enhanced_analyze_code(code_sample)
    dynamic_results = run_dynamic_analysis(code_sample)
    explainer = AIExplainer()
    explanation = explainer.explain_analysis_results(static_results, dynamic_results)
    
    print(f"\\n📊 Results Summary:")
    print(f"  • Static issues: {len(static_results.get('issues', []))}")
    print(f"  • Runtime success: {dynamic_results.success}")  
    print(f"  • AI explanation: {explanation['title']}")
    print(f"  • Category: {explanation['category']}")


if __name__ == "__main__":
    demo_integrated_analysis()
    demo_api_usage()
