# Lumina: AI Powered Bug Explainer

Learn to debug smarter with Lumina, an educational tool combining enhanced static and dynamic code analysis with AI powered explanations to help developers and learners understand why bugs happen.

## 🚀 Project Overview

Lumina is an early stage prototype for students and developers who want to master debugging fundamentals. By combining static code analysis, runtime tracing, and AI driven explanations, Lumina goes beyond surface level fixes to provide clear, educational insights.

## 🔍 Key Features

### 1) Enhanced Static Analysis

* Advanced AST parsing for common bug patterns:

  * Potential `IndexError` from out‑of‑bounds indexing.
  * Security risks like `eval()` usage.
  * Poor exception handling (e.g., bare `except:`).
  * Debugging leftovers like empty `print()` statements.
  * Missing function docstrings / overly complex functions.
* Complexity metrics (cyclomatic complexity) to flag risky code.
* Variable usage tracker for potentially unused variables.
* Outputs in structured JSON or emoji rich console text.

### 2) Dynamic Analysis with Execution Tracing

* Safe, sandboxed code execution that captures runtime errors.
* Line by line tracing with local variables and call stack depth.
* Execution stats (time, lines executed, functions called).
* Helpful context around exceptions to make fixes clearer.

### 3) AI Explainer Module

* Explanations generated from the static + dynamic results.
* Focuses on *why* an issue happened and how to prevent it.
* Ready to plug in real model APIs (OpenAI, Gemini).

### 4) Command‑Line Interface

* Analyze a file or run a set of demo bugs.
* JSON or human readable output.
* Verbose logging when you want more detail.
* Optional API key input for future AI integration.

### 🧪 Tests & CI

* Pytest suite (\~11 unit + integration tests).
* \~40% coverage across core modules.
* GitHub Actions runs tests on every push.

## 📦 Project Structure

```
lumina-ai-debugger/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── src/
│   ├── static_analysis.py        # Enhanced static analysis module
│   ├── dynamic_analysis.py       # Dynamic execution tracing module
│   ├── ai_explainer.py           # AI explanation engine
│   └── main.py                   # CLI interface integrating modules
├── scripts/
│   └── demo_enhanced_analysis.py # Demo script for static analysis
├── sample_bugs/                  # Educational bug examples
│   ├── index_error.py
│   ├── logic_error.py
│   ├── syntax_error.py
│   ├── type_error.py
│   └── complexity_issue.py
├── tests/                        # Automated tests
│   ├── __init__.py
│   ├── test_static_analysis.py
│   ├── test_dynamic_analysis.py
│   ├── test_ai_explainer.py
│   ├── test_cli.py
│   └── test_integration.py
├── .github/
│   └── workflows/
│       └── test.yml              # CI on push
└── docs/                         # (Future documentation)
```

## 🛠️ Getting Started

Requires Python 3.13+.

### Setup

```
git clone https://github.com/akashdevbuilds/Lumina-ai-debugger
cd lumina-ai-debugger
python -m venv venv
source venv/bin/activate

# Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### Available Commands

Run from the project root using the CLI module:

```
python -m src.main --help
```

Displays:

```
usage: main.py [-h] [--analyze ANALYZE] [--demo] [--json] [--verbose] [--api-key API_KEY]

Lumina: AI Debugger CLI

optional arguments:
  -h, --help          show this help message and exit
  --analyze ANALYZE   Path to Python file to analyze
  --demo              Run demo analysis on sample bug files
  --json              Output results in JSON format
  --verbose           Enable verbose logging
  --api-key API_KEY   API key for future AI integration
```

### Examples

#### Run demo analysis on sample bugs

```
python -m src.main --demo
```

*Output (partial):*

```
=== Demo: syntax_error.py ===
Syntax valid: False
Syntax Error on line 35: invalid decimal literal

=== Demo: type_error.py ===
Syntax valid: True
Issues found: 0
Execution success: True
AI Explanation: No major issues detected in your code.
```

#### Analyze a specific file with JSON output

```
python -m src.main --analyze sample_bugs/index_error.py --json
```

*Sample JSON output:*

```
{
  "static_analysis": {
    "syntax_valid": true,
    "issues": [
      {
        "type": "missing_docstring",
        "severity": "medium",
        "line": 2,
        "message": "Function \"divide\" lacks documentation",
        "pattern": "undocumented_function"
      }
    ],
    "functions": [
      {
        "name": "divide",
        "line": 2,
        "args": 2,
        "has_docstring": false
      }
    ],
    "metrics": {
      "total_lines": 9,
      "function_count": 1,
      "issues_found": 1
    }
  },
  "dynamic_analysis": {
    "success": true,
    "trace": [...],
    "exec_time": 0.007
  },
  "ai_explanation": {
    "simple_explanation": "Your code has minor documentation issues. No runtime errors detected."
  }
}
```

### Run Tests

```
pytest               # run all tests
pytest --cov=src     # coverage
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## 🛣️ Roadmap - Coming Soon 

* Real AI model integration (Gemini) with env based API keys.
* Web UI (Flask) for interactive analysis.
* Multi file project support.
* Performance improvements and caching.
* Docker setup for deployment.

## 👥 Contributing & Feedback

Active student project. Contributions, suggestions, and bug reports are welcome!

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (add tests when relevant)
4. Open a Pull Request with a brief description

## 📜 License

MIT License

Thank you for exploring Lumina! Learn smarter debugging ; understand the *why* behind bugs, not just the fix.
