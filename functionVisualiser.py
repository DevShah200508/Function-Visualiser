import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import transformation as tr
from vector import Vector 
from colorama import Fore, Style
from custom import custom_is_constant
from matplotlib.widgets import Slider, CheckButtons, RadioButtons, Button
from time import sleep
from random import uniform, randint

RADIOBUTTON_LABELS = ["Rotation", "Shearing", "Scaling", "Reflection", "Translation"]
SLIDER_POS_1 = [0.1, 0.1, 0.65, 0.03]
SLIDER_POS_2 = [0.1, 0.15, 0.65, 0.03]
SLIDER_POS_3 = [0.1, 0.20, 0.65, 0.03]

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
                func = sp.lambdify(x, expr, 'numpy')
                test_valid_function(func)
                funcs.append(sp.lambdify(x, expr, 'numpy'))
                labels.append(f"f{i}: {str(expr)}")
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
            bounds = input("Input bounds of x and y in the form min_x, max_x, min_y, max_y (separeted by ','): ").split(",")
            if len(bounds) != 4:
                raise ValueError
            min_x, max_x, min_y, max_y = [float(num) for num in bounds]
            if (max_x <= min_x) or (max_y <= min_y):
                raise ValueError
            return min_x, max_x, min_y, max_y
        except TypeError:
            print(Fore.LIGHTMAGENTA_EX + 'Make sure you input a whole numbers!' + Style.RESET_ALL)
        except ValueError:
            print(Fore.LIGHTMAGENTA_EX + 'Make sure you choose a valid range (only 4 values inputted), maximum value cannot be smaller than minimum value!' + Style.RESET_ALL)

# Main function
def main():
    func_arr, func_labels = get_function(get_function_numbers()) # Retrieve all user inputted functions 
    min_x, max_x, min_y, max_y = get_axis_lim() # Get the axis limits for the domain and range of the graph you want displayed 
    value = int(np.ceil(max(100 + abs(max_x), 100 + abs(min_x)))) # Ensures function is plotted out the visible view of the graph 
    x = np.linspace(-value, value, num= value*20) 

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.3, bottom=0.35)
    lines = [] # Stores all functions/lines
    selected_lines = [] # Stores all the functions selected for transformation
    current_sliders = [] # Stores all the current sliders needing to be displayed on the screen

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

    # Creation of initial sliders and buttons for all the neccessary transformations on a function
    ax_rotation_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
    rotation_slider = Slider(ax_rotation_slider, 'Rotation', -360, 360, valinit=0.0)

    ax_rotation_center_x_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
    rotation_center_x_slider = Slider(ax_rotation_center_x_slider, 'Rotation center (x)', min_x, max_x, valinit=(min_x+max_x)/2)

    ax_rotation_center_y_slider = plt.axes(SLIDER_POS_3, facecolor='lightgoldenrodyellow')
    rotation_center_y_slider = Slider(ax_rotation_center_y_slider, 'Rotation center (y)', min_y, max_y, valinit=(min_y+max_y)/2)

    current_sliders.extend([rotation_slider, rotation_center_x_slider, rotation_center_y_slider])

    ax_transformation_selector = plt.axes([0.01, 0.35, 0.2, 0.2], facecolor='lightgreen')
    transformation_selector = RadioButtons(ax_transformation_selector, RADIOBUTTON_LABELS)

    ax_function_selector = plt.axes([0.01, 0.6, 0.2, 0.2], facecolor='lightgoldenrodyellow')
    visibility = [True] * len(func_arr)
    function_selector = CheckButtons(ax_function_selector, func_labels, visibility)

    # Method to deal with change in the rotation sliders
    def update_rotation(val) -> None:
        angle = rotation_slider.val
        center_x, center_y = rotation_center_x_slider.val, rotation_center_y_slider.val 
        for line in selected_lines:
            index = lines.index(line)
            f = func_arr[index]
            x_transformed, y_transformed = tr.transform_values(x, f(x), tr.rotation, Vector(2, [center_x, center_y]), angle * tr.PI/180)
            line.set_xdata(x_transformed)
            line.set_ydata(y_transformed)
        
        fig.canvas.draw_idle()

    def transformation_selection(label) -> None:
        for slider in current_sliders:
            slider.ax.remove()
        current_sliders.clear()

        match label:
            case "Rotation":
                ax_rotation_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
                rotation_slider = Slider(ax_rotation_slider, 'Rotation', -360, 360, valinit=0.0)

                ax_rotation_center_x_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
                rotation_center_x_slider = Slider(ax_rotation_center_x_slider, 'Rotation center (x)', min_x, max_x, valinit=(min_x+max_x)/2)

                ax_rotation_center_y_slider = plt.axes(SLIDER_POS_3, facecolor='lightgoldenrodyellow')
                rotation_center_y_slider = Slider(ax_rotation_center_y_slider, 'Rotation center (y)', min_y, max_y, valinit=(min_y+max_y)/2)

                current_sliders.extend([rotation_slider, rotation_center_x_slider, rotation_center_y_slider])
            case "Shearing":
                ax_shearing_kx_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
                shearing_kx_slider = Slider(ax_shearing_kx_slider, 'kx shearing', -10, 10, valinit=1.0)

                ax_shearing_ky_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
                shearing_ky_slider = Slider(ax_shearing_ky_slider, 'ky shearing', -10, 10, valinit=1.0)
                current_sliders.extend([shearing_kx_slider, shearing_ky_slider])
            case "Scaling": 
                ax_scaling_kx_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
                scaling_kx_slider = Slider(ax_scaling_kx_slider, 'kx scaling', -10, 10, valinit=1.0)

                ax_scaling_ky_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
                scaling_ky_slider = Slider(ax_scaling_ky_slider, 'ky scaling', -10, 10, valinit=1.0)
                current_sliders.extend([scaling_kx_slider, scaling_ky_slider])
            case "Reflection":
                ax_reflection_x_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
                reflection_x_slider = Slider(ax_reflection_x_slider, 'x reflection', -1, 1, valinit=1.0)

                ax_reflection_y_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
                reflection_y_slider = Slider(ax_reflection_y_slider, 'y reflection', -1, 1, valinit=0.0)
                current_sliders.extend([reflection_x_slider, reflection_y_slider])
            case _:
                ax_translation_x_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
                translation_x_slider = Slider(ax_translation_x_slider, 'x translation', min_x, max_x, valinit=0.0)

                ax_translation_y_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
                translation_y_slider = Slider(ax_translation_y_slider, 'y translation', min_y, max_y, valinit=0.0)
                current_sliders.extend([translation_x_slider, translation_y_slider])            

    
    # Method to deal with changes to functions being selected 
    def toggle_plot(label) -> None:
        index = func_labels.index(label) # Finds the index of the label within func_labels
        line = lines[index] # Finds the corresponding plot/line which matches the label

        if line in selected_lines:
            selected_lines.remove(line) # Remove line as it is being toggled off
            line.set_alpha(0.3) # Set non selected lines to transparent 
        else:
            selected_lines.append(line) # Add line as it is being toggled on
            line.set_alpha(1.0) # Set selected lines to

        fig.canvas.draw_idle()

    # Calls the handler functions when an event occurs 
    rotation_slider.on_changed(update_rotation)
    rotation_center_x_slider.on_changed(update_rotation)
    rotation_center_y_slider.on_changed(update_rotation)
    transformation_selector.on_clicked(transformation_selection)
    function_selector.on_clicked(toggle_plot)

    plt.show()

if __name__ == "__main__":
    main()
