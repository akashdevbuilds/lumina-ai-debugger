import traceback

def run_code(code_str):
    try:
        exec(code_str, {})
    except Exception:
        return traceback.format_exc()
    return "Code ran successfully."

if __name__ == "__main__":
    buggy_code = "def add(a, b):\n return a + b\n\nprint(add(1))"  # Missing second arg, triggers error
    result = run_code(buggy_code)
    print(result)
