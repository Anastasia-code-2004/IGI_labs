import input


def calculate_sum_and_product(lst):
    """Calculate the sum of non-negative elements between the min and max elements of the list"""
    min_abs_index = min(range(len(lst)), key=lambda i: abs(lst[i]))
    max_abs_index = max(range(len(lst)), key=lambda i: abs(lst[i]))

    if min_abs_index > max_abs_index:
        min_abs_index, max_abs_index = max_abs_index, min_abs_index

    sum_between = sum(num for num in lst[min_abs_index + 1:max_abs_index] if num >= 0)
    product_between = 1
    for num in lst[min_abs_index+1:max_abs_index]:  # calculate the product of elements between min and max
        product_between *= num
    return sum_between, product_between


def input_process_output():
    """Input the list of float numbers, calculate the sum of non-negative elements between the min and max elements"""
    size = input.check_list_size_input()
    print('Do you want to fill the list yourself or use a generator?')  # ask the user how to fill the list
    print('1. Manually')
    print('2. Generator')
    choice = input.get_user_choice_task5_menu()
    lst = []
    if choice == 1:
        input.input_list_by_user(lst, size)
    elif choice == 2:
        input.initialize_list_with_generator(lst, size)
    s, p = calculate_sum_and_product(lst)
    print(lst)
    print(f'Sum of non-negative elements between min and max elements: {s}')
    print(f'Product of elements between min and max elements: {p}')
