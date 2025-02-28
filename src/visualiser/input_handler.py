import sympy as sp
from .error_handler import handle_error, reset_error_box
from src.custom import custom_is_constant, custom_test_valid_function, custom_get_random_color
from typing import Optional

# Method to retrieve function from user input. Constant k for k functions. Colors are chosen randomly. Labels are returned for visual information
def get_functions(window, labels=None) -> Optional[tuple]:
    if labels is None:
        labels = []
    funcs = []
    function_number = len(window.function_entries)
    try:
        if function_number == 0:    
            raise ValueError
    except ValueError:
        handle_error(window, 'Please select between 1-8 functions before trying to plot!')
        return
    for i in range(function_number):
        user_input = window.function_entries[i].get()
        try:
            expr = sp.sympify(user_input)
            if (isinstance(expr, sp.Symbol) and user_input != "x") or custom_is_constant(user_input):
                raise sp.SympifyError
            x = sp.symbols("x")
            func = sp.lambdify(x, expr, 'numpy')
            custom_test_valid_function(func)
            funcs.append(func)
            labels.append(f"f{i}: {str(expr)}")
        except:
            handle_error(window, 'Invalid form of function, make sure function is valid and all variables are denoted with the letter "x". Ensure no only constant input! Try again...')
            return
    reset_error_box(window)
    return funcs, labels

# Method to take the visual bounds of the graph from the user
def get_axis_lim(window) -> Optional[tuple]:
    user_input = [window.min_x_bound.get(), window.max_x_bound.get(), window.min_y_bound.get(), window.max_y_bound.get()]
    try:
        if any(input == "" for input in user_input):
            raise ValueError
    except ValueError:
        handle_error(window, 'Please ensure to input a value for each bound')

        return
    try:
        min_x, max_x, min_y, max_y = [float(bound) for bound in user_input]
        if (max_x <= min_x) or (max_y <= min_y):
            raise ValueError
        reset_error_box(window)
        return min_x, max_x, min_y, max_y
    except TypeError:
        handle_error(window, 'Make sure you input a whole number!')
    except ValueError:
        handle_error(window, 'Make sure you choose a valid range, maximum value cannot be smaller than minimum value!')
