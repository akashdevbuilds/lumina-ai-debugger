"""
Bug Category: Code Complexity - Hard to maintain and understand
Difficulty: Intermediate-Advanced
Learning Focus: Code organization, function design, cyclomatic complexity
Common Cause: Trying to do too much in one function, nested conditions

High complexity makes code error-prone and hard to debug.
This function has very high cyclomatic complexity.
"""

def overly_complex_processor(data, mode, options, debug=False):
    """
    This function tries to do everything - it's a complexity nightmare!
    Cyclomatic complexity is extremely high due to multiple nested conditions.
    
    This is an example of what NOT to do in real code.
    """
    
    results = []
    errors = []
    processed_count = 0
    
    # Start of the complexity nightmare - too many nested conditions
    if data:
        if isinstance(data, list):
            if len(data) > 0:
                for item in data:
                    if isinstance(item, dict):
                        if 'id' in item:
                            if mode == 'process':
                                if 'value' in item:
                                    if item['value'] is not None:
                                        if isinstance(item['value'], (int, float)):
                                            if item['value'] > 0:
                                                if options.get('multiply', False):
                                                    if options.get('factor', 1) > 1:
                                                        result = item['value'] * options['factor']
                                                        if debug:
                                                            print(f"Multiplied {item['value']} by {options['factor']} = {result}")
                                                        if result < 1000:
                                                            results.append(result)
                                                            processed_count += 1
                                                        else:
                                                            errors.append(f"Result too large: {result}")
                                                    else:
                                                        errors.append(f"Factor not > 1: {options.get('factor', 1)}")
                                                elif options.get('add', False):
                                                    if 'increment' in options:
                                                        if options['increment'] > 0:
                                                            result = item['value'] + options['increment']
                                                            if debug:
                                                                print(f"Added {options['increment']} to {item['value']} = {result}")
                                                            results.append(result)
                                                            processed_count += 1
                                                        else:
                                                            errors.append(f"Increment must be positive: {options['increment']}")
                                                    else:
                                                        errors.append(f"No increment specified for item {item['id']}")
                                                elif options.get('square', False):
                                                    result = item['value'] ** 2
                                                    if debug:
                                                        print(f"Squared {item['value']} = {result}")
                                                    results.append(result)
                                                    processed_count += 1
                                                else:
                                                    results.append(item['value'])
                                                    processed_count += 1
                                            elif item['value'] == 0:
                                                if options.get('include_zero', False):
                                                    results.append(0)
                                                    processed_count += 1
                                                else:
                                                    errors.append(f"Zero value in item {item['id']}")
                                            else:
                                                errors.append(f"Negative value in item {item['id']}: {item['value']}")
                                        else:
                                            errors.append(f"Value is not a number in item {item['id']}: {type(item['value'])}")
                                    else:
                                        errors.append(f"Null value in item {item['id']}")
                                else:
                                    errors.append(f"Missing 'value' field in item {item['id']}")
                            elif mode == 'validate':
                                if 'value' in item and 'name' in item:
                                    if isinstance(item['value'], (int, float)):
                                        if isinstance(item['name'], str):
                                            if item['value'] >= 0:
                                                if len(item['name']) > 0:
                                                    if item['name'].isalpha():
                                                        results.append(True)
                                                        processed_count += 1
                                                    else:
                                                        results.append(False)
                                                        errors.append(f"Name contains non-alphabetic chars: {item['name']}")
                                                else:
                                                    results.append(False)
                                                    errors.append(f"Empty name in item {item['id']}")
                                            else:
                                                results.append(False)
                                                errors.append(f"Negative value in item {item['id']}")
                                        else:
                                            results.append(False)
                                            errors.append(f"Name is not string in item {item['id']}")
                                    else:
                                        results.append(False)
                                        errors.append(f"Value is not number in item {item['id']}")
                                else:
                                    results.append(False)
                                    errors.append(f"Missing required fields in item {item['id']}")
                            elif mode == 'count':
                                if 'type' in item:
                                    if item['type'] == 'countable':
                                        results.append(1)
                                        processed_count += 1
                                    else:
                                        results.append(0)
                                else:
                                    results.append(0)
                            elif mode == 'filter':
                                if 'category' in item:
                                    if options.get('allowed_categories'):
                                        if item['category'] in options['allowed_categories']:
                                            results.append(item)
                                            processed_count += 1
                                        else:
                                            errors.append(f"Category not allowed: {item['category']}")
                                    else:
                                        results.append(item)
                                        processed_count += 1
                                else:
                                    errors.append(f"Missing category in item {item['id']}")
                            else:
                                errors.append(f"Unknown mode: {mode}")
                        else:
                            errors.append("Item missing 'id' field")
                    elif isinstance(item, (int, float)):
                        if mode == 'process':
                            if item > 0:
                                results.append(item * 2)
                                processed_count += 1
                            else:
                                results.append(0)
                        else:
                            errors.append(f"Numeric item in non-process mode: {item}")
                    else:
                        errors.append(f"Item is not dict or number: {type(item)}")
            else:
                errors.append("Data list is empty")
        elif isinstance(data, dict):
            # Another complex branch for dict handling...
            if 'items' in data:
                if mode == 'process':
                    for key, value in data['items'].items():
                        if isinstance(value, (int, float)):
                            if value > 0:
                                if options.get('normalize', False):
                                    if 'max_value' in options:
                                        normalized = value / options['max_value']
                                        results.append(normalized)
                                        processed_count += 1
                                    else:
                                        errors.append("Normalization requested but no max_value provided")
                                else:
                                    results.append(value * 2)
                                    processed_count += 1
                            else:
                                results.append(0)
                        elif isinstance(value, str):
                            if len(value) > 0:
                                if options.get('string_to_length', False):
                                    results.append(len(value))
                                    processed_count += 1
                                else:
                                    results.append(value)
                                    processed_count += 1
                            else:
                                errors.append(f"Empty string for key {key}")
                        else:
                            errors.append(f"Unsupported type for key {key}: {type(value)}")
            else:
                errors.append("Dict missing 'items' field")
        else:
            errors.append(f"Unsupported data type: {type(data)}")
    else:
        errors.append("No data provided")
    
    # Even more complexity for result post-processing
    if results:
        if mode == 'process' and options.get('sort_results', False):
            if options.get('reverse_sort', False):
                results.sort(reverse=True)
            else:
                results.sort()
        
        if options.get('limit_results', False):
            if 'max_results' in options:
                if options['max_results'] > 0:
                    results = results[:options['max_results']]
                else:
                    errors.append("max_results must be positive")
    
    return {
        'results': results,
        'errors': errors,
        'processed_count': processed_count,
        'success_rate': processed_count / (processed_count + len(errors)) if (processed_count + len(errors)) > 0 else 0
    }

# This function should be broken into smaller, focused functions:
# - validate_item()
# - process_numeric_item()
# - process_dict_item()
# - apply_options()
# - post_process_results()
# etc.

if __name__ == "__main__":
    # Test the overly complex function
    test_data = [
        {'id': 1, 'value': 10, 'name': 'test1'},
        {'id': 2, 'value': 20, 'name': 'test2'},
        {'id': 3, 'value': -5, 'name': 'test3'},  # This will cause issues
    ]
    
    result = overly_complex_processor(
        data=test_data,
        mode='process',
        options={'multiply': True, 'factor': 2, 'debug': True},
        debug=True
    )
    
    print("Complexity Demo Results:")
    print(f"Processed: {result['processed_count']} items")
    print(f"Errors: {len(result['errors'])} errors")
    print(f"Success rate: {result['success_rate']:.2%}")
    
    if result['errors']:
        print("\nErrors encountered:")
        for error in result['errors'][:3]:  # Show first 3 errors
            print(f"  - {error}")
