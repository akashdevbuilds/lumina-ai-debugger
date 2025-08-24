import pytest
from src.ai_explainer import AIExplainer


def test_ai_explainer_basic():
    explainer = AIExplainer()

    static_result = {'syntax_valid': True, 'issues': []}
    dynamic_result = {'success': True}
    code = "print('hello')"

    result = explainer.explain_analysis_results(static_result, dynamic_result, code)
    assert 'simple_explanation' in result
    assert isinstance(result['simple_explanation'], str)


def test_ai_explainer_with_syntax_error():
    explainer = AIExplainer()

    static_result = {
        'syntax_valid': False,
        'syntax_error': {'type': 'SyntaxError', 'message': 'invalid syntax'}
    }
    dynamic_result = {'success': False}
    code = "if True\n    print('missing colon')"

    result = explainer.explain_analysis_results(static_result, dynamic_result, code)
    assert 'simple_explanation' in result
    assert isinstance(result['simple_explanation'], str) and len(result['simple_explanation']) > 0
