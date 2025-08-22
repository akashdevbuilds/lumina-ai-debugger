# Lumina: AI-Powered Bug Explainer

Learn to debug smarter with Lumina ,an educational tool combining enhanced static and dynamic code analysis with AI-powered explanations to help developers and learners understand why bugs happen.

---

## 🚀 Project Overview

Lumina is an early stage prototype designed for students and developers interested in mastering debugging fundamentals. By combining static code analysis, runtime dynamic tracing, and AI driven explanations, Lumina goes beyond surface level fixes to provide deep educational insights.

---

## 🔍 Key Features

### 1. Enhanced Static Analysis  
- Advanced AST parsing to detect common bug patterns including:  
  - Potential `IndexError` from out-of-bounds indexing  
  - Security risks like `eval()` usage  
  - Poor exception handling (e.g., bare `except:` clauses)  
  - Debugging leftovers like empty `print()` statements  
  - Missing function docstrings and overly complex functions  
- Complexity metrics (cyclomatic complexity) to identify risky code parts  
- Variable usage tracker to highlight potentially unused variables  
- Structured JSON and emoji-rich console output formats  

### 2. Dynamic Analysis with Execution Tracing  
- Safe sandboxed code execution capturing runtime errors  
- Detailed line by line tracing with local variable states and call stack depth  
- Execution performance metrics (total time, lines executed, functions called)  
- Rich context for runtime exceptions to aid understanding  

### 3. AI Explainer Module  
- Educational feedback generated from static and dynamic results  
- Helps users learn why issues happen and how to fix/prevent them  
- Ready to be extended with real AI model APIs (e.g., OpenAI, Gemini)  

### 4. Professional Command-Line Interface (CLI)  
- Analyze individual Python files or run demos on curated educational bugs  
- Supports JSON or human readable text outputs  
- Verbose logging option for deeper insights  
- API key input for future AI integration  

---

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
├── tests/                       # (Future automated tests)
└── docs/                        # (Future documentation)
```

---

## 🛠️ Getting Started

### Setup

```
git clone https://github.com/akashdevbuilds/Lumina-ai-debugger
cd lumina-ai-debugger
python -m venv venv
source venv/bin/activate      # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### Available Commands

Run commands from the project root, using the CLI interface in `src/main.py` as a module:

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

#### Run demo analysis on sample bugs:

```
python -m src.main --demo
```

_Output (partial):_

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

#### Analyze a specific Python file with JSON output:

```
python -m src.main --analyze sample_bugs/index_error.py --json
```

_Sample JSON output:_

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

---

## 🛣️ Roadmap & Next Steps

- **Multifile project support** for advanced analysis  
- **Real AI model integration** with API keys (OpenAI, Gemini)  
- **Web UI development** for interactive debugging  
- **Comprehensive automated testing** and CI/CD setup  
- **Performance and security enhancements** for sandboxed execution  

---

## 👥 Contributing & Feedback

This is an active student project. Contributions, suggestions, and bug reports are welcome!

1. Fork the repo  
2. Create a feature branch (`git checkout -b feature/my-feature`)  
3. Commit your changes  
4. Open a Pull Request with detailed description  

---

## 📜 License

MIT License

---

Thank you for exploring Lumina! Learn smarter debugging — understand the *why* behind bugs, not just the fix.

---
