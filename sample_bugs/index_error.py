"""
Bug Category: IndexError - Array bounds violation
Difficulty: Beginner
Learning Focus: Loop boundaries, list indexing, range() function
Common Cause: Off-by-one errors, incorrect range calculations

This is one of the most common beginner mistakes in Python.
The loop tries to access an index that doesn't exist.
"""

def buggy_list_access():
    """Function demonstrating IndexError bug pattern"""
    fruits = ['apple', 'banana', 'orange']
    print("Accessing fruits:")
    
    # BUG: range(4) tries to access indices 0, 1, 2, 3
    # But fruits only has indices 0, 1, 2 (length = 3)
    for i in range(4):  # Should be range(3) or range(len(fruits))
        print(f"Fruit {i}: {fruits[i]}")  # Will crash on i=3
    
    print("Done!")

def another_buggy_pattern():
    """Another common IndexError pattern"""
    numbers = [10, 20, 30]
    
    # BUG: Using len() as index - it's always one too many!
    last_index = len(numbers)  # This is 3, but max valid index is 2
    print(f"Last number: {numbers[last_index]}")  # IndexError!

# This will crash with: IndexError: list index out of range
if __name__ == "__main__":
    try:
        buggy_list_access()
    except IndexError as e:
        print(f"❌ Error in buggy_list_access: {e}")
    
    try:
        another_buggy_pattern()
    except IndexError as e:
        print(f"❌ Error in another_buggy_pattern: {e}")
