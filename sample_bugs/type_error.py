"""
Bug Category: TypeError - Incorrect data type operations
Difficulty: Beginner
Learning Focus: Python data types, type checking, string vs number operations
Common Cause: Mixing incompatible types, incorrect input handling

Python is dynamically typed but still requires compatible operations.
"""

def concatenate_with_number(text, number):
    """Try to combine text and number - WITH BUGS!"""
    
    # BUG: Can't directly concatenate string and integer
    result = text + number  # TypeError: can only concatenate str (not "int") to str
    return result

def calculate_price(base_price, tax_rate):
    """Calculate total price including tax - WITH BUGS!"""
    
    # Simulate getting input (usually from user/file)
    base_price = "100"  # BUG: This should be converted to float/int
    tax_rate = "0.08"   # BUG: This should be converted to float
    
    # BUG: Trying to do math with strings
    tax_amount = base_price * tax_rate  # Will repeat string, not multiply
    total = base_price + tax_amount     # String concatenation instead of addition
    
    return total

def process_ages(age_list):
    """Process a list of ages - WITH BUGS!"""
    adult_ages = []
    
    for age in age_list:
        # BUG: Comparing string to number
        if age > 18:  # TypeError if age is string
            adult_ages.append(age)
    
    return adult_ages

def divide_numbers(a, b):
    """Divide two numbers - WITH BUGS!"""
    # BUG: No type checking - will fail with strings
    result = a / b  # TypeError if a or b are strings
    return result

# These will crash with TypeErrors
if __name__ == "__main__":
    try:
        result1 = concatenate_with_number("Score: ", 95)
        print(result1)
    except TypeError as e:
        print(f"❌ Error 1: {e}")
    
    try:
        price = calculate_price("100", "0.08")
        print(f"Total price: {price}")
    except TypeError as e:
        print(f"❌ Error 2: {e}")
    
    try:
        adults = process_ages(["25", "16", "30", "12"])  # Strings, not integers
        print(f"Adults: {adults}")
    except TypeError as e:
        print(f"❌ Error 3: {e}")
    
    try:
        result = divide_numbers("100", "5")  # Strings, not numbers
        print(f"Division result: {result}")
    except TypeError as e:
        print(f"❌ Error 4: {e}")
