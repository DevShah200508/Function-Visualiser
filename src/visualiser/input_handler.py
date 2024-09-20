import sympy as sp
from src.custom import custom_is_constant, custom_test_valid_function, custom_get_random_color


# Method to retrieve function from user input. Constant k for k functions. Colors are chosen randomly. Labels are returned for visual information
def get_functions(window, labels=[]) -> tuple:
    funcs = []
    for i in range(len(window.function_entries)):
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
            break
        except (sp.SympifyError, TypeError):
            print("hello first error in get_function")
            window.error_label.configure(text='   Invalid form of function, make sure function is valid and all variables are denoted with the letter "x". Ensure no only constant input! Try again...', image=window.error_icon)
    window.error_label.configure(text="", image="")
    return funcs, labels

# Method to take the visual bounds of the graph from the user
def get_axis_lim(window) -> tuple:
    try:
        min_x, max_x, min_y, max_y = float(window.min_x_bound.get()), float(window.max_x_bound.get()), float(window.min_y_bound.get()), float(window.max_y_bound.get())
        if (max_x <= min_x) or (max_y <= min_y):
            raise ValueError
        window.error_label.configure(text="", image="")
        return min_x, max_x, min_y, max_y
    except TypeError:
        print("Type error in get_axis_lim")
        window.error_label.configure(text='   Make sure you input a whole numbers!', image=window.error_icon)
    except ValueError:
        print("ValueError in get_axis_lim")
        window.error_label.configure(text='   Make sure you choose a valid range (only 4 values inputted), maximum value cannot be smaller than minimum value!', image=window.error_icon)
