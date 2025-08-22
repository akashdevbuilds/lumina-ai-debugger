"""
Enhanced Dynamic Analysis for Lumina AI Debugger

Provides comprehensive runtime analysis including execution tracing,
variable tracking, performance monitoring, and intelligent error detection.
"""

import sys
import time
import traceback
import io
import ast
import gc
import resource
from contextlib import redirect_stdout, redirect_stderr
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ExecutionResult:
    """Comprehensive result of dynamic code execution"""
    success: bool
    output: str
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    traceback_info: Optional[str] = None
    execution_time: float = 0.0
    memory_peak: int = 0
    trace_data: List[Dict[str, Any]] = None
    performance_metrics: Dict[str, Any] = None
    variable_history: Dict[str, List[Any]] = None
    function_calls: List[Dict[str, Any]] = None


class ExecutionTracer:
    """Advanced execution tracer for comprehensive runtime analysis"""
    
    def __init__(self, max_entries: int = 500):
        self.trace_data: List[Dict[str, Any]] = []
        self.call_stack: List[str] = []
        self.start_time: float = 0.0
        self.max_entries = max_entries
        self.variable_history: Dict[str, List[Any]] = defaultdict(list)
        self.function_calls: List[Dict[str, Any]] = []
        self.line_coverage: set = set()
        
    def trace_calls(self, frame, event, arg):
        """Main trace function called by sys.settrace"""
        # Stop if too many entries to prevent memory issues
        if len(self.trace_data) >= self.max_entries:
            return None
            
        # Only trace user code, skip system and library code
        filename = frame.f_code.co_filename
        if "<" in filename or "site-packages" in filename:
            return self.trace_calls

        # Capture timestamp on first event
        if not self.start_time:
            self.start_time = time.time()

        # Record local variables safely
        local_vars = {}
        for name, val in frame.f_locals.items():
            if not name.startswith("__"):
                try:
                    # Limit string representation length
                    val_repr = repr(val)
                    if len(val_repr) > 100:
                        val_repr = val_repr[:97] + "..."
                    local_vars[name] = val_repr
                    
                    # Track variable changes
                    if event == 'line':
                        self.variable_history[name].append({
                            'value': val_repr,
                            'line': frame.f_lineno,
                            'timestamp': time.time() - self.start_time
                        })
                except Exception:
                    local_vars[name] = f"<unrepr-able {type(val).__name__}>"

        # Create trace entry
        entry = {
            "event": event,
            "function": frame.f_code.co_name,
            "line": frame.f_lineno,
            "locals": local_vars,
            "stack_depth": len(self.call_stack),
            "timestamp": time.time() - self.start_time,
            "filename": filename
        }

        # Handle different event types
        if event == "call":
            func_name = frame.f_code.co_name
            self.call_stack.append(func_name)
            
            # Record function call
            call_info = {
                'name': func_name,
                'line': frame.f_lineno,
                'args': {k: v for k, v in local_vars.items() if not k.startswith('_')},
                'timestamp': time.time() - self.start_time
            }
            self.function_calls.append(call_info)
            
        elif event == "return":
            if self.call_stack:
                self.call_stack.pop()
            try:
                entry["return_value"] = repr(arg) if arg is not None else "None"
            except:
                entry["return_value"] = f"<unrepr-able {type(arg).__name__}>"
                
        elif event == "line":
            # Track line coverage
            self.line_coverage.add(frame.f_lineno)

        self.trace_data.append(entry)
        return self.trace_calls

    def get_summary(self) -> Dict[str, Any]:
        """Generate summary of execution trace"""
        if not self.trace_data:
            return {}
            
        return {
            'total_events': len(self.trace_data),
            'functions_called': len(set(entry['function'] for entry in self.trace_data if entry['event'] == 'call')),
            'lines_covered': len(self.line_coverage),
            'max_stack_depth': max((entry['stack_depth'] for entry in self.trace_data), default=0),
            'execution_time': max((entry['timestamp'] for entry in self.trace_data), default=0),
            'variable_changes': len(self.variable_history)
        }


class DynamicAnalyzer:
    """Main dynamic analysis engine"""
    
    def __init__(self, timeout: float = 5.0, memory_limit: int = 100 * 1024 * 1024):
        self.timeout = timeout
        self.memory_limit = memory_limit  # 100MB default
        
    def analyze_code(self, code: str, inputs: Optional[List[str]] = None) -> ExecutionResult:
        """Perform comprehensive dynamic analysis of code"""
        
        # Pre-execution validation
        try:
            ast.parse(code)
        except SyntaxError as e:
            return ExecutionResult(
                success=False,
                output="",
                error_type="SyntaxError",
                error_message=str(e),
                traceback_info=traceback.format_exc()
            )
        
        # Setup execution environment
        tracer = ExecutionTracer()
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        # Capture output
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            # Setup tracing
            sys.settrace(tracer.trace_calls)
            
            # Create execution namespace
            exec_globals = {
                '__builtins__': __builtins__,
                'input': self._mock_input(inputs or []),
            }
            exec_locals = {}
            
            # Execute code with output capture
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, exec_globals, exec_locals)
            
            # Success case
            execution_time = time.time() - start_time
            peak_memory = self._get_memory_usage() - start_memory
            
            return ExecutionResult(
                success=True,
                output=stdout_capture.getvalue(),
                execution_time=execution_time,
                memory_peak=max(0, peak_memory),
                trace_data=tracer.trace_data,
                performance_metrics=tracer.get_summary(),
                variable_history=dict(tracer.variable_history),
                function_calls=tracer.function_calls
            )
            
        except Exception as e:
            # Error case
            execution_time = time.time() - start_time
            peak_memory = self._get_memory_usage() - start_memory
            
            return ExecutionResult(
                success=False,
                output=stdout_capture.getvalue(),
                error_type=type(e).__name__,
                error_message=str(e),
                traceback_info=traceback.format_exc(),
                execution_time=execution_time,
                memory_peak=max(0, peak_memory),
                trace_data=tracer.trace_data,
                performance_metrics=tracer.get_summary(),
                variable_history=dict(tracer.variable_history),
                function_calls=tracer.function_calls
            )
            
        finally:
            # Clean up tracing
            sys.settrace(None)
            
    def _mock_input(self, inputs: List[str]):
        """Create mock input function for testing"""
        input_iter = iter(inputs)
        
        def mock_input(prompt=""):
            try:
                return next(input_iter)
            except StopIteration:
                return ""  # Return empty string when inputs exhausted
                
        return mock_input
    
    def _get_memory_usage(self) -> int:
        """Get current memory usage in bytes"""
        try:
            return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024  # Convert to bytes
        except:
            return 0
    
    def analyze_performance_patterns(self, result: ExecutionResult) -> Dict[str, Any]:
        """Analyze performance patterns from execution result"""
        if not result.trace_data:
            return {}
            
        patterns = {
            'potential_issues': [],
            'recommendations': [],
            'complexity_indicators': {}
        }
        
        # Analyze execution patterns
        if result.performance_metrics:
            metrics = result.performance_metrics
            
            # Check for potential infinite loops
            if metrics.get('total_events', 0) > 10000:
                patterns['potential_issues'].append({
                    'type': 'potential_infinite_loop',
                    'severity': 'high',
                    'description': 'Extremely high number of execution events detected'
                })
            
            # Check for deep recursion
            if metrics.get('max_stack_depth', 0) > 100:
                patterns['potential_issues'].append({
                    'type': 'deep_recursion',
                    'severity': 'medium', 
                    'description': f"Maximum stack depth of {metrics['max_stack_depth']} detected"
                })
            
            # Performance recommendations
            if result.execution_time > 1.0:
                patterns['recommendations'].append(
                    'Consider optimizing algorithm - execution time exceeded 1 second'
                )
                
            if result.memory_peak > 50 * 1024 * 1024:  # 50MB
                patterns['recommendations'].append(
                    'High memory usage detected - consider memory optimization'
                )
        
        return patterns
    
    def get_execution_flow(self, result: ExecutionResult) -> List[str]:
        """Extract simplified execution flow from trace data"""
        if not result.trace_data:
            return []
            
        flow = []
        for entry in result.trace_data:
            if entry['event'] in ['call', 'return']:
                indent = "  " * entry['stack_depth']
                if entry['event'] == 'call':
                    flow.append(f"{indent}→ {entry['function']}() [line {entry['line']}]")
                else:
                    ret_val = entry.get('return_value', 'None')
                    flow.append(f"{indent}← returns {ret_val}")
        
        return flow


def run_dynamic_analysis(code: str, inputs: Optional[List[str]] = None, 
                        timeout: float = 5.0) -> ExecutionResult:
    """Convenience function for running dynamic analysis"""
    analyzer = DynamicAnalyzer(timeout=timeout)
    return analyzer.analyze_code(code, inputs)


# Demo and testing functions
def demo_dynamic_analysis():
    """Demonstrate the enhanced dynamic analysis capabilities"""
    print("🚀 Enhanced Dynamic Analysis Demo")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            'name': 'Simple Function',
            'code': '''
def greet(name):
    return f"Hello, {name}!"

result = greet("World")
print(result)
'''
        },
        {
            'name': 'Loop with Variables',
            'code': '''
total = 0
for i in range(5):
    total += i
    print(f"Step {i}: total = {total}")
print(f"Final total: {total}")
'''
        },
        {
            'name': 'Error Case',
            'code': '''
def divide(a, b):
    return a / b

result1 = divide(10, 2)
print(f"10 / 2 = {result1}")

result2 = divide(10, 0)  # This will cause ZeroDivisionError
print(f"10 / 0 = {result2}")
'''
        }
    ]
    
    analyzer = DynamicAnalyzer()
    
    for test in test_cases:
        print(f"\n📝 Testing: {test['name']}")
        print("-" * 30)
        
        result = analyzer.analyze_code(test['code'])
        
        # Display results
        print(f"✅ Success: {result.success}")
        print(f"⏱️  Execution Time: {result.execution_time:.4f}s")
        print(f"🧠 Memory Peak: {result.memory_peak:,} bytes")
        
        if result.output:
            print(f"📤 Output:\n{result.output}")
            
        if not result.success:
            print(f"❌ Error: {result.error_type}: {result.error_message}")
            
        if result.performance_metrics:
            metrics = result.performance_metrics
            print(f"📊 Metrics:")
            print(f"  • Events: {metrics.get('total_events', 0)}")
            print(f"  • Functions: {metrics.get('functions_called', 0)}")
            print(f"  • Lines covered: {metrics.get('lines_covered', 0)}")
            print(f"  • Max stack depth: {metrics.get('max_stack_depth', 0)}")
        
        # Show execution flow for interesting cases
        if test['name'] in ['Simple Function', 'Error Case']:
            flow = analyzer.get_execution_flow(result)
            if flow:
                print(f"🔄 Execution Flow:")
                for step in flow[:10]:  # Limit output
                    print(f"  {step}")
                if len(flow) > 10:
                    print(f"  ... and {len(flow) - 10} more steps")


if __name__ == "__main__":
    demo_dynamic_analysis()
