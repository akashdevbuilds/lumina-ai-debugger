"""
Bug Category: Logic Error - Incorrect algorithm
Difficulty: Intermediate
Learning Focus: Algorithm correctness, edge cases, mathematical operations
Common Cause: Misunderstanding requirements, incorrect formulas

Logic errors are tricky because the code runs without crashing,
but produces wrong results.
"""

def calculate_average(numbers):
    """Calculate average of a list of numbers - WITH BUGS!"""
    
    # BUG 1: Doesn't handle empty list properly
    if len(numbers) == 0:
        return 0  # Should return None or raise ValueError
    
    total = 0
    for num in numbers:
        total += num
    
    # BUG 2: Adds 1 to the result for no reason
    average = (total / len(numbers)) + 1  # The +1 is wrong!
    
    return average

def find_maximum(numbers):
    """Find the largest number in a list - WITH BUGS!"""
    
    # BUG 3: Starts with 0 instead of first element
    max_num = 0  # Wrong! What if all numbers are negative?
    
    for num in numbers:
        if num > max_num:
            max_num = num
    
    return max_num

def count_vowels(text):
    """Count vowels in text - WITH BUGS!"""
    vowels = 'aeiou'
    count = 0
    
    for char in text:
        # BUG 4: Case sensitivity - misses uppercase vowels
        if char in vowels:  # Should be char.lower() in vowels
            count += 1
    
    return count

# Test cases that reveal the bugs
if __name__ == "__main__":
    print("Testing calculate_average:")
    print(f"Average of [1, 2, 3]: {calculate_average([1, 2, 3])}")  # Should be 2.0, returns 3.0
    print(f"Average of []: {calculate_average([])}")  # Should be None or error, returns 0
    
    print("\nTesting find_maximum:")
    print(f"Max of [1, 5, 3]: {find_maximum([1, 5, 3])}")  # Correct: 5
    print(f"Max of [-5, -2, -10]: {find_maximum([-5, -2, -10])}")  # Should be -2, returns 0!
    
    print("\nTesting count_vowels:")
    print(f"Vowels in 'Hello': {count_vowels('Hello')}")  # Should be 2 (e,o), returns 1
    print(f"Vowels in 'AEIOU': {count_vowels('AEIOU')}")  # Should be 5, returns 0!
