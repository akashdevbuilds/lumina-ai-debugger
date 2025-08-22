# 🎯 Lumina: AI-Powered Bug Explainer (Day 1 Prototype) (Student Personal Project)

Learn to debug better with AI-powered explanations (early-stage prototype)

## 🚧 Current Project Status (Day 1)

This is an early prototype focusing on:

- **Enhanced Static Analysis** Advanced AST parsing with comprehensive bug pattern detection, complexity analysis, and code quality metrics
- Dynamic Analysis Prototype Docker-based sandbox executing code snippets safely and capturing runtime exceptions  
- Command Line Interface (CLI Simple prototype to run analysis on sample buggy code  
- Educational Vision Designing for learners to grasp debugging concepts through layered analysis  

Note AI-powered explanations and advanced analysis features are still under development.

## 🏗️ System Architecture (Planned)

```
Lumina Analysis Pipeline:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Static Analysis │ -> │ Dynamic Tracing  │ -> │ AI Explanation  │
│  (AST parsing)  │    │ (Sandbox runtime)│    │ (Planned)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔍 Enhanced Static Analysis Features

The enhanced static analysis system provides comprehensive code analysis including:

### Bug Pattern Detection
- **IndexError Detection:** Identifies potential array bound violations (e.g., `range(len(list) + 1)`)
- **Security Risks:** Detects dangerous `eval()` usage
- **Exception Handling:** Finds bare `except:` clauses that are too broad
- **Debug Artifacts:** Identifies leftover debug code like empty `print()` statements
- **Code Quality:** Detects missing function docstrings and overly long functions

### Code Analysis Features
- **Complexity Analysis:** Cyclomatic complexity calculation with risk classification
- **Variable Tracking:** Identifies potentially unused variables
- **Function Analysis:** Detailed function metrics and documentation validation
- **Code Metrics:** Lines of code, comments, and structural analysis
- **Severity Classification:** Issues categorized as Critical, High, Medium, or Low

### Output Formats
- **Visual Console Output:** Emoji-enhanced reports for human reading
- **Structured JSON:** Machine-readable format for tool integration
- **Backward Compatibility:** Maintains compatibility with existing analysis functions

## 🏃 How to Get Started

```bash
# Clone and set up virtual environment
git clone https://github.com/akashdevbuilds/lumina-ai-debugger
cd lumina-ai-debugger
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Run enhanced static analysis on sample buggy code
python src/static_analysis.py

# Run the comprehensive analysis demo
python demo_enhanced_analysis.py

# Run dynamic execution sandbox prototype
python src/dynamic_analysis.py
```


## 🎯 Target Audience

Ideal for:

- Students and developers interested in debugging fundamentals  
- Learners who want to understand "why" bugs happen  
- Anyone curious about combining static and dynamic analysis  

Not yet suitable for:  
- Production debugging workflows  
- Complex multi-file projects  
- Complete AI-powered explanations (coming soon!)  

## 🔄 Roadmap & Next Steps

Planned enhancements include:

- ✅ **COMPLETED:** Enhanced static analysis with advanced bug detection patterns
- Building an AI explainer module to generate educational feedback  
- Integrating execution tracing with richer runtime data  
- Adding a clean CLI with multi-stage analysis flow  
- Developing a web UI for interactive debugging  
- Real AI model integration (OpenAI,Gemini)  
- Comprehensive testing and documentation

💡 Why Lumina Is Different!

Lumina is an early-stage prototype focused on helping learners understand why bugs occur rather than just providing quick fixes. It uses a multi-stage approach that combines basic static analysis with sandboxed code execution to give insight into code behavior, though these features are still being developed. Designed with beginner developers and students in mind, Lumina aims to support learning debugging fundamentals by offering educational explanations and guidance as the project evolves. This student project explores how AI can assist in debugging in a more insightful and educational way, with many planned features yet to be implemented.

## 🤝 Contributing & Feedback

This is a personal student project in active development. Contributions, suggestions, and feedback are warmly welcomed!

1. Fork the repo  
2. Create a branch (`git checkout -b feature/my-feature`)  
3. Commit and push your changes  
4. Open a Pull Request with description  

## 📄 License
MIT License
