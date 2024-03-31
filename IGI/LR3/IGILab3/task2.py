import input


def count_even_numbers(numbers):
    """Count the number of even numbers in the list."""
    count = 0
    for num in numbers:
        if num % 2 == 0:
            count += 1
    return count


def input_output_even_numbers():
    """Input natural numbers from the user and count the number of even numbers in the list."""
    numbers = []
    input.input_natural_numbers(numbers)
    count = count_even_numbers(numbers)
    print('Amount of even natural numbers: ', count)
