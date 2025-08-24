# API Documentation

## Static Analysis Module

### `enhanced_analyze_code(code: str) -> Dict`
Performs comprehensive static analysis on Python code.

**Parameters:**
- `code`: Python source code as string

**Returns:**
- Dictionary with syntax validation, issues, functions, complexity metrics

## Dynamic Analysis Module

### `run_code_with_tracing(code: str) -> Dict`
Executes code in sandbox with detailed tracing.

**Parameters:**
- `code`: Python source code as string

**Returns:**
- Dictionary with execution results, trace data, performance metrics

## AI Explainer Module

### `explain_analysis_results(static_result, dynamic_result, code) -> Dict`
Generates educational explanations from analysis results.

**Parameters:**
- `static_result`: Output from static analysis
- `dynamic_result`: Output from dynamic analysis  
- `code`: Original source code

**Returns:**
- Dictionary with simple and detailed explanations
