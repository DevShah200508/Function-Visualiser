import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import transformation as tr
from vector import Vector 
from colorama import Fore, Style
from custom import custom_is_constant
from matplotlib.widgets import Slider, CheckButtons
from time import sleep
from random import uniform, randint

# Test a 100 different random values between -1000 and 1000 to see if function inputted is actually valid 
def test_valid_function(f) -> None:
    for _ in range(100):
        float(f(randint(-1000, 1000)))

# Method to retrieve function from user input. Constant k for k functions. Colors are chosen randomly. Labels are returned for visual information
def get_function(k: int, labels=[]):
    funcs = []
    print("Input a function in terms of x (no constants!), (Use (* /) for multiplication/division, (+ -) for addition and subtraction and (**) for powers, exp(x) for e^x)")
    sleep(2)
    for i in range(k):
        while True:
            u_input = input(f"f{i}(x) = ")
            try:
                expr = sp.sympify(u_input)
                if (isinstance(expr, sp.Symbol) and u_input != "x") or custom_is_constant(u_input):
                    raise sp.SympifyError(f"'{u_input}' is not a valid mathematical expression.")
                x = sp.symbols("x")
                labels.append(f"f{i}(x) = {str(expr)}")
                func = sp.lambdify(x, expr, 'numpy')
                test_valid_function(func)
                funcs.append(sp.lambdify(x, expr, 'numpy'))
                break
            except (sp.SympifyError, TypeError):
                print(Fore.LIGHTMAGENTA_EX + 'Invalid form of function, make sure function is valid and all variables are denoted with the letter "x" and no constants are inputted! Try again...' + Style.RESET_ALL)
                sleep(2)
    return funcs, labels

# Method to retrieve the number of functions being plotted from user input
def get_function_numbers() -> int:
    while True:
        try:
            k = int(input("Please input the number of functions you want to plot (maximum 8 functions): "))
            if (k < 1) or (k > 8):
                raise ValueError
            return k
        except TypeError:
            print(Fore.LIGHTMAGENTA_EX + 'Make sure you input a whole number!' + Style.RESET_ALL)
            sleep(2.0)
        except ValueError:
            print(Fore.LIGHTMAGENTA_EX + 'Make sure you input a number between 1 to 8 (inclusive)!' + Style.RESET_ALL)

# Function which returns a tuple containing random rgb values for a random color
def get_random_color() -> tuple:
    r = uniform(0, 1)
    g = uniform(0, 1)
    b = uniform(0, 1)
    return (r, g, b)

def get_axis_lim() -> tuple:
    while True:
        try:
            min_x = int(input("What is the minimum value of x you want displayed? "))
            max_x = int(input("What is the maximum value of x you want displayed? "))
            min_y = int(input("What is the minimum value of y you want displayed? "))
            max_y = int(input("What is the maximum value of y you want displayed? "))
            if (max_x <= min_x) or (max_y <= min_y):
                raise ValueError
            return min_x, max_x, min_y, max_y
        except TypeError:
            print(Fore.LIGHTMAGENTA_EX + 'Make sure you input a whole numbers!' + Style.RESET_ALL)
        except ValueError:
            print(Fore.LIGHTMAGENTA_EX + 'Make sure you choose a valid range, maximum value cannot be smaller than minimum value!' + Style.RESET_ALL)

# Main function
def main():
    func_arr, func_labels = get_function(get_function_numbers()) # Retrieve all user inputted functions 
    min_x, max_x, min_y, max_y = get_axis_lim() # Get the axis limits for the domain and range of the graph you want displayed 
    value = 100
    x = np.linspace(-value, value, num=value*20)

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.3, bottom=0.35)
    lines = [] # Stores all functions/lines
    selected_lines = [] # Stores all the functions selected for transformation

    # Plotting the initial functions
    for i, f in enumerate(func_arr):
        line, = ax.plot(x, f(x), color=get_random_color(), label=func_labels[i]) # Unpack a single item tuple using ,
        lines.append(line) # Append the line object in the array of lines
        selected_lines.append(line) # Initially select all the lines
    
    # Basic set up for the visuals of the graph
    plt.rcParams["font.size"] = 7.5
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.axhline(0, color='black',linewidth=1.5)
    ax.axvline(0, color='black',linewidth=1.5)
    ax.set_title('Plot of functions')
    ax.grid(True)
    ax.legend()

    # Creation of sliders and buttons for all the neccessary transformations on a function
    ax_rotation_slider = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    rotation_slider = Slider(ax_rotation_slider, 'Rotation', -360, 360, valinit=0.0)

    ax_rotation_center_x_slider = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    rotation_center_x_slider = Slider(ax_rotation_center_x_slider, 'Rotation_center_x', -10, 10, valinit=0.0)

    ax_rotation_center_y_slider = plt.axes([0.1, 0.20, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    rotation_center_y_slider = Slider(ax_rotation_center_y_slider, 'Rotation_center_y', -10, 10, valinit=0.0)


    """ax_scaling_slider_x = plt.axes([0.1, 0.20, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    scaling_slider_x = Slider(ax_scaling_slider_x, 'Scaling_x', -10.0, 10.0, valinit=1.0)

    ax_scaling_slider_y = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    scaling_slider_y = Slider(ax_scaling_slider_y, 'Scaling_y', -10.0, 10.0, valinit=1.0)"""

    ax_function_selector = plt.axes([0.05, 0.4, 0.2, 0.2], facecolor='lightgoldenrodyellow')
    visibility = [True] * len(func_arr)
    function_selector = CheckButtons(ax_function_selector, func_labels, visibility)

    # Method to deal with change in the rotation sliders
    def update_rotation(val):
        angle = rotation_slider.val
        center_x, center_y = rotation_center_x_slider.val, rotation_center_y_slider.val 
        for line in selected_lines:
            index = lines.index(line)
            f = func_arr[index]
            x_transformed, y_transformed = tr.transform_values(x, f(x), tr.rotation, Vector(2, [center_x, center_y]), angle * tr.PI/180)
            line.set_xdata(x_transformed)
            line.set_ydata(y_transformed)
        
        fig.canvas.draw_idle()
    
    # Method to deal with changes to functions being selected 
    def toggle_plot(label):
        index = func_labels.index(label) # Finds the index of the label within func_labels
        line = lines[index] # Finds the corresponding plot/line which matches the label

        if line in selected_lines:
            selected_lines.remove(line) # Remove line as it is being toggled off
            line.set_alpha(0.3) # Set non selected lines to transparent 
        else:
            selected_lines.append(line) # Add line as it is being toggled on
            line.set_alpha(1.0) # Set selected lines to

        fig.canvas.draw_idle()

    # Calls the update function when value of slider/button is changed 
    rotation_slider.on_changed(update_rotation)
    rotation_center_x_slider.on_changed(update_rotation)
    rotation_center_y_slider.on_changed(update_rotation)
    function_selector.on_clicked(toggle_plot)

    plt.show()

if __name__ == "__main__":
    main()
