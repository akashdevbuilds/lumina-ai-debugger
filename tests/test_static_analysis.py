import pytest
from src.static_analysis import enhanced_analyze_code

def test_syntax_valid_code():
    code = "def hello():\n    return 'world'"
    result = enhanced_analyze_code(code)
    assert result['syntax_valid'] == True
    if 'syntax_error' in result:
        assert result['syntax_error'] is None

def test_syntax_invalid_code():
    code = "def hello(\n    return 'world'"
    result = enhanced_analyze_code(code)
    assert result['syntax_valid'] == False
    assert result['syntax_error'] is not None

def test_detect_eval_usage():
    code = "eval('print(hello)')"
    result = enhanced_analyze_code(code)
    issues = result['issues']
    eval_issues = [i for i in issues if i['type'] == 'eval_usage']
    assert len(eval_issues) > 0
