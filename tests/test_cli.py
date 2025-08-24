import pytest
import subprocess
import json

def test_cli_help():
    result = subprocess.run(['python', '-m', 'src.main', '--help'],
                          capture_output=True, text=True)
    assert result.returncode == 0
    assert 'Lumina: AI Debugger CLI' in result.stdout

def test_cli_demo():
    result = subprocess.run(['python', '-m', 'src.main', '--demo'],
                          capture_output=True, text=True)
    assert result.returncode == 0
