def get_user_choice_main_menu():
    """Get user choice from the main menu."""
    while True:
        try:
            user_input = int(input('Enter a number from 1 to 5 to choose a task, or 0 to exit: '))
            if 0 <= user_input <= 5:
                return user_input
            else:
                print('Invalid input. Please enter a number from 0 to 5.')
        except ValueError:
            print('Invalid input. Please enter a number.')


def input_natural_numbers(numbers):
    """Input natural numbers from the user."""
    while True:
        try:
            num = int(input('Enter a natural number or 0 to exit: '))
            if num == 0:
                break
            elif num > 0:
                numbers.append(num)
        except ValueError:
            print('Invalid input. Please enter a natural number.')
    return numbers


def input_float_number():
    """Input a float number from the user."""
    while True:
        try:
            num = float(input())
            return num
        except ValueError:
            print('Invalid input. Please enter a float number.')


def get_user_choice_task5_menu():
    """Get user choice from the task5 menu."""
    while True:
        try:
            user_input = int(input('Enter a number 1 or 2: '))
            if user_input == 1 or user_input == 2:
                return user_input
            else:
                print('Invalid input. Please enter a number 1 or 2.')
        except ValueError:
            print('Invalid input. Please enter a number.')


def check_list_size_input():
    """Check the size of the list input from the user."""
    while True:
        try:
            size = int(input('Enter the size of the list: '))
            if size > 0:
                return size
            else:
                print('Invalid input. The size of the list must be a positive integer.')
        except ValueError:
            print('Invalid input. Please enter an integer.')


def input_list_by_user(lst, size):
    """Input a list of float numbers from the user."""
    while True:
        try:
            if len(lst) == size:
                break
            num = float(input('Enter a number: '))
            lst.append(num)
        except ValueError:
            print('Invalid input. Please enter a float number.')


def float_generator(size):
    """Generate float numbers from 1.25 to size + 1.25."""
    for i in range(size):
        yield float(i) + 1.25


def initialize_list_with_generator(lst, size):
    """Initialize a list with float numbers using a generator."""
    for num in float_generator(size):
        lst.append(num)
