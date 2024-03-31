import math, input


def sin_series(x, eps):
    """Calculate the sum of the series for the sine function."""
    sin_x = 0
    n = 0
    a = x
    while abs(a) > eps:  # cycle until the next term is less than the accuracy
        sin_x += a
        n += 1
        a *= -x ** 2 / (2 * n) / (2 * n + 1)
    return sin_x, n


def input_output_decomposition():
    """Input x and accuracy, calculate the sum of the series for the sine function and compare
    it with the math.sin(x)."""
    print('Enter x: ')
    x = input.input_float_number()
    print('Enter accuracy: ')
    eps = input.input_float_number()
    if eps <= 0:
        print('Accuracy must be greater than 0.')
        return
    sin_my, n = sin_series(x, eps)
    print(f"| {'x':^10} | {'n':^10} | {'F(x)':^20} | {'Math F(x)':^20} | {'eps':^10} |")  # table header
    print(f"| {x:^10.2f} | {n:^10} | {sin_my:^20.10f} | {math.sin(x):^20.10f} | {eps:^10.2e} |")
