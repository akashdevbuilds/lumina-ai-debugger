import sys
from io import StringIO
from src.main import main

def test_full_pipeline_demo():
    """Test the complete analysis pipeline with demo code"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        sys.argv = ['main.py', '--demo']
        main()
        output = captured_output.getvalue()
        # Updated assertion to check for expected keywords in actual output
        assert 'Syntax valid:' in output
        assert 'AI Explanation:' in output
    finally:
        sys.stdout = old_stdout
