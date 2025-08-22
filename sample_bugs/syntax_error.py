"""
Bug Category: SyntaxError - Invalid Python syntax
Difficulty: Beginner
Learning Focus: Python syntax rules, proper indentation, matching brackets
Common Cause: Typos, missing colons, incorrect indentation, unmatched brackets

Syntax errors prevent Python from even parsing your code.
These must be fixed before the program can run.

NOTE: This file contains intentional syntax errors for educational purposes.
It won't run as-is - that's the point!
"""

# BUG 1: Missing colon after if statement
def check_age(age):
    if age >= 18  # Missing colon here!
        return "Adult"
    else:
        return "Minor"

# BUG 2: Incorrect indentation
def greet_user(name):
    if name:
        print(f"Hello, {name}!")
print("Welcome!")  # Wrong indentation - should be inside the function

# BUG 3: Unmatched parentheses
def calculate_area(radius):
    pi = 3.14159
    area = pi * (radius ** 2  # Missing closing parenthesis
    return area

# BUG 4: Invalid variable name (starts with number)
def process_data():
    2nd_value = 10  # Variable names can't start with numbers
    return 2nd_value

# BUG 5: Missing quotes around string
def display_message():
    message = Hello World  # Missing quotes around string
    print(message)

# BUG 6: Inconsistent indentation (mixing tabs and spaces)
def calculate_total(items):
    total = 0
    for item in items:
        total += item  # This line uses different indentation
	return total  # This line uses tab instead of spaces

# Note: This file demonstrates syntax errors that prevent code execution
# Python will show detailed syntax error messages for each issue
