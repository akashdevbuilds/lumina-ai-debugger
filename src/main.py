#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from src.static_analysis import enhanced_analyze_code
from src.dynamic_analysis import run_code_with_tracing
from src.ai_explainer import AIExplainer

class LuminaCLI:
    def __init__(self, api_key=None, verbose=False):
        self.explainer = AIExplainer(api_key)
        self.verbose = verbose

    def analyze_file(self, filepath, json_output=False):
        path = Path(filepath)
        if not path.exists() or path.suffix != '.py':
            print(f"Error: File not found or not a .py file: {filepath}")
            sys.exit(1)

        code = path.read_text()
        # Static
        static_res = enhanced_analyze_code(code)
        # Dynamic (if syntax valid)
        dynamic_res = run_code_with_tracing(code) if static_res.get('syntax_valid') else None
        # AI Explanation
        explanation = self.explainer.explain_analysis_results(static_res, dynamic_res, code)

        results = {
            'static_analysis': static_res,
            'dynamic_analysis': dynamic_res,
            'ai_explanation': explanation
        }

        if json_output:
            print(json.dumps(results, indent=2))
        else:
            self.print_results(results)

    def run_demo(self, json_output=False):
        demo_files = list(Path('sample_bugs').glob('*.py'))[:3]
        for f in demo_files:
            print(f"\n=== Demo: {f.name} ===")
            self.analyze_file(f, json_output)

    def print_results(self, res):
        sa = res['static_analysis']
        print(f"Syntax valid: {sa.get('syntax_valid')}")
        if not sa.get('syntax_valid'):
            err = sa.get('syntax_error', {})
            print(f"Syntax Error on line {err.get('line')}: {err.get('message')}")
            return
        print(f"Issues found: {len(sa.get('issues', []))}")
        if res['dynamic_analysis']:
            da = res['dynamic_analysis']
            print(f"Execution success: {da.get('success')}")
        ae = res['ai_explanation']
        print(f"AI Explanation: {ae.get('simple_explanation')}")

def main():
    parser = argparse.ArgumentParser(description="Lumina: AI Debugger CLI")
    parser.add_argument('--analyze', help="Path to Python file to analyze")
    parser.add_argument('--demo', action='store_true', help="Run demo on sample bugs")
    parser.add_argument('--json', action='store_true', help="Output JSON instead of text")
    parser.add_argument('--verbose', action='store_true', help="Verbose logging")
    parser.add_argument('--api-key', help="API key for real AI integration")
    args = parser.parse_args()

    cli = LuminaCLI(api_key=args.api_key, verbose=args.verbose)

    if args.demo:
        cli.run_demo(json_output=args.json)
    elif args.analyze:
        cli.analyze_file(args.analyze, json_output=args.json)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
