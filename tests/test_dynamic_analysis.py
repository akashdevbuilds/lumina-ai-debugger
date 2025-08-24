import pytest
from src.dynamic_analysis import run_code_with_tracing

def test_successful_execution():
    code = "print('Hello World')"
    result = run_code_with_tracing(code)
    assert result['success'] == True
    assert 'exec_time' in result

def test_runtime_error():
    code = "x = [1,2,3]\nprint(x[10])"  # IndexError
    result = run_code_with_tracing(code)
    assert result['success'] == False
    assert 'IndexError' in str(result.get('error', ''))
