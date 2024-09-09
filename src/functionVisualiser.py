import sys 
import warnings
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import transformation as tr
from vector import Vector 
from colorama import Fore, Style
from custom import custom_is_constant, custom_test_valid_function, custom_get_random_color
from matplotlib.widgets import Slider, CheckButtons, RadioButtons, Button
from time import sleep

# Constants that are used later within the script
RADIOBUTTON_LABELS = ["Rotation", "Shearing", "Scaling", "Reflection", "Translation"]
SCALE_POINT_X, SCALE_POINT_Y = 1/15, 1/15
POINT_INCH_SCALE = 1/72
SLIDER_POS_1 = [0.1, 0.10, 0.65, 0.03]
SLIDER_POS_2 = [0.1, 0.15, 0.65, 0.03]
SLIDER_POS_3 = [0.1, 0.20, 0.65, 0.03]
INITIAL_RESET_SLIDER_POS = [0.85, 0.12, 0.1, 0.1]

# Method to retrieve function from user input. Constant k for k functions. Colors are chosen randomly. Labels are returned for visual information
def get_function(k: int, labels=[]) -> tuple:
    funcs = []
    print("Input a function in terms of x (no constants!), (Use (* /) for multiplication/division, (+ -) for addition and subtraction and (**) for powers, exp(x) for e^x)")
    sleep(1)
    for i in range(k):
        while True:
            user_input = input(f"f{i}(x): ")
            if (user_input == "exit"):
                sys.exit()
            try:
                expr = sp.sympify(user_input)
                if (isinstance(expr, sp.Symbol) and user_input != "x") or custom_is_constant(user_input):
                    raise sp.SympifyError(f"'{user_input}' is not a valid mathematical expression.")
                x = sp.symbols("x")
                func = sp.lambdify(x, expr, 'numpy')
                custom_test_valid_function(func)
                funcs.append(func)
                labels.append(f"f{i}: {str(expr)}")
                break
            except (sp.SympifyError, TypeError):
                print(Fore.LIGHTMAGENTA_EX + 'Invalid form of function, make sure function is valid and all variables are denoted with the letter "x". Ensure no only constant input! Try again...' + Style.RESET_ALL)
                sleep(2)
    return funcs, labels

# Method to retrieve the number of functions being plotted from user input
def get_function_numbers() -> int:
    while True:
        try:
            user_input = input("Please input the number of functions you want to plot (maximum 8 functions): ")
            if (user_input == "exit"):
                sys.exit()
            k = int(user_input)
            if (k < 1) or (k > 8):
                raise ValueError
            return k
        except TypeError:
            print(Fore.LIGHTMAGENTA_EX + 'Make sure you input a whole number!' + Style.RESET_ALL)
            sleep(2.0)
        except ValueError:
            print(Fore.LIGHTMAGENTA_EX + 'Make sure you input a number between 1 to 8 (inclusive)!' + Style.RESET_ALL)

# Method to take the visual bounds of the graph from the user
def get_axis_lim() -> tuple:
    while True:
        try:
            bounds = input("Input bounds of x and y in the form min_x, max_x, min_y, max_y (separeted by ',', and with opening and closing '()'): ").strip("()").split(",")
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

# Method to hide widgets from the screen and deactivate them
def hide_widgets(widgets) -> None:
    for widget in widgets:
        widget.set_active(False)
        widget.ax.set_visible(False)       
          
# Method to show widgets on the screen and activate them
def show_widgets(widgets) -> None:
    for widget in widgets:
        widget.set_active(True)
        widget.ax.set_visible(True)          

# Main function
def visualiser_main():
    print(Fore.LIGHTGREEN_EX + "Welcome to the visual function transformer, you can exit at any point by typing 'exit' in the command line" + Style.RESET_ALL)
    sleep(1.0)
    func_arr, func_labels = get_function(get_function_numbers()) # Retrieve all user inputted functions 
    min_x, max_x, min_y, max_y = get_axis_lim() # Get the axis limits for the domain and range of the graph you want displayed 
    value = int(np.ceil(max(100 + abs(max_x), 100 + abs(min_x)))) # Ensures function is plotted out the visible view of the graph 
    x = np.linspace(-value, value, num= value*50) 

    lines = [] # Stores all functions/lines
    selected_lines = [] # Stores all the functions selected for transformation
    current_widgets = [] # Stores all the current widgets needing to be displayed on the screen
    initial_data = [] # Stores all the initial (x, y) state(s) of the graph, useful when resetting the graph
    points = [] # Stores all the drawn markers/points

    fig, ax = plt.subplots() # Automatically make subplots within the main plot
    plt.subplots_adjust(left=0.3, bottom=0.35) # Create space for buttons and sliders

    # Plotting the initial functions
    for i, f in enumerate(func_arr):
        y = f(x)
        initial_data.append((x, y))
        line, = ax.plot(x, y, color=custom_get_random_color(), label=func_labels[i]) # Unpack a single item tuple using ,
        lines.append(line) # Append the line object in the array of lines
        selected_lines.append(line) # Initially select all the lines

    current_data = initial_data[:] # This stores the current (x, y) data state of all the functions at any given time
    rotation_center_point, = ax.plot((min_x+max_x)/2, (min_y+max_y)/2, color="black", marker="x") # Mark for the center point of rotation
    reflection_line, = ax.plot(x, [0]*len(x), linestyle='--', color='grey', label='Line of reflection') # Line of reflection
    reflection_line.set_visible(False)

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
    fig.text(0.10, 0.95, "Function transformer", fontsize=20, fontweight='bold', ha="center", va="center")
    fig.text(0.13, 0.90, "• Use Ctrl + LMB to mark points and Ctrl + RMB to remove marked points from the axes.", fontsize=8, ha="center", va="center") 
    fig.text(0.13, 0.88, "• Toggle the function(s) you want to transform and select a transformation below.", fontsize=8, ha="center", va="center")
    fig.text(0.13, 0.86, "• Use the sliders to vary the parameters of the specified transformation.", fontsize=8, ha="center", va="center")

    # Creation of initial sliders for all the neccessary transformations on a function
    ax_rotation_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
    rotation_slider = Slider(ax_rotation_slider, 'Rotation', -360, 360, valinit=0.0)

    ax_rotation_center_x_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
    rotation_center_x_slider = Slider(ax_rotation_center_x_slider, 'Rotation center (x)', min_x, max_x, valinit=(min_x+max_x)/2)

    ax_rotation_center_y_slider = plt.axes(SLIDER_POS_3, facecolor='lightgoldenrodyellow')
    rotation_center_y_slider = Slider(ax_rotation_center_y_slider, 'Rotation center (y)', min_y, max_y, valinit=(min_y+max_y)/2)

    # Set up the sliders for the shearing 
    ax_shearing_kx_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
    shearing_kx_slider = Slider(ax_shearing_kx_slider, 'kx shearing', -10, 10, valinit=0.0)

    ax_shearing_ky_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
    shearing_ky_slider = Slider(ax_shearing_ky_slider, 'ky shearing', -10, 10, valinit=0.0)

    # Set up the sliders for scaling 
    ax_scaling_kx_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
    scaling_kx_slider = Slider(ax_scaling_kx_slider, 'kx scaling', -10, 10, valinit=1.0)

    ax_scaling_ky_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
    scaling_ky_slider = Slider(ax_scaling_ky_slider, 'ky scaling', -10, 10, valinit=1.0)

    # Set up the sliders and button for reflection
    ax_reflection_x_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
    reflection_x_slider = Slider(ax_reflection_x_slider, 'x reflection', -1, 1, valinit=1.0)

    ax_reflection_y_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
    reflection_y_slider = Slider(ax_reflection_y_slider, 'y reflection', -1, 1, valinit=0.0)

    ax_reflection_button = plt.axes([0.85, 0.17, 0.1, 0.1], facecolor='lightblue')
    reflection_button = Button(ax_reflection_button, label="Reflect", hovercolor='dodgerblue')

    # Set up the sliders for translation
    ax_translation_x_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
    translation_x_slider = Slider(ax_translation_x_slider, 'x translation', -abs(max_x-min_x), abs(max_x-min_x), valinit=0.0)

    ax_translation_y_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
    translation_y_slider = Slider(ax_translation_y_slider, 'y translation', -abs(max_y-min_y), abs(max_y-min_y), valinit=0.0)

    # Add the rotation sliders into the current sliders list as this will be the initial chosen transformation
    current_widgets.extend([rotation_slider, rotation_center_x_slider, rotation_center_y_slider])

    # Hide all the sliders which are not involved with rotation 
    hide_widgets([shearing_kx_slider, shearing_ky_slider, scaling_kx_slider, scaling_ky_slider, reflection_x_slider, reflection_y_slider, reflection_button, translation_x_slider, translation_y_slider])

    # CheckButtons and RadioButtons for selecting function(s) and transformation(s)
    ax_transformation_selector = plt.axes([0.01, 0.35, 0.2, 0.2], facecolor='lightgreen')
    transformation_selector = RadioButtons(ax_transformation_selector, RADIOBUTTON_LABELS)

    ax_function_selector = plt.axes([0.01, 0.6, 0.2, 0.2], facecolor='lightgoldenrodyellow')
    visibility = [True] * len(func_arr)
    function_selector = CheckButtons(ax_function_selector, func_labels, visibility)
    
    # Button for resetting any transformations to the plot 
    ax_reset_button = plt.axes(INITIAL_RESET_SLIDER_POS, facecolor='lightblue')
    reset_button = Button(ax_reset_button, label="Reset", hovercolor='dodgerblue')

    # Method to deal with change in the rotation sliders
    def update_rotation(val) -> None:
        angle = rotation_slider.val
        center_x, center_y = rotation_center_x_slider.val, rotation_center_y_slider.val
        update_rotation_center_point(center_x, center_y) # Update the position of the center point the axes
        for line in selected_lines:
            index = lines.index(line)
            x0, y0 = current_data[index]
            x1, y1 = tr.transform_values(x0, y0, tr.rotation, Vector([center_x, center_y]), angle * tr.PI/180)
            line.set_xdata(x1)
            line.set_ydata(y1)
        
        fig.canvas.draw_idle()
    
    # Method to deal with change in the rotation_center sliders
    def update_rotation_center_point(center_x: float, center_y: float) -> None:
        rotation_center_point.set_xdata([center_x])
        rotation_center_point.set_ydata([center_y])

    # Method to deal with change in the shearing sliders
    def update_shearing(val) -> None:
        kx, ky = shearing_kx_slider.val, shearing_ky_slider.val
        for line in selected_lines:
            index = lines.index(line)
            x0, y0 = current_data[index]
            x1, y1 = tr.transform_values(x0, y0, tr.shearing, kx, ky)
            line.set_xdata(x1)
            line.set_ydata(y1)
        
        fig.canvas.draw_idle()

    # Method to deal with change in the scaling sliders
    def update_scaling(val) -> None:
        kx, ky = scaling_kx_slider.val, scaling_ky_slider.val
        for line in selected_lines:
            index = lines.index(line)
            x0, y0 = current_data[index]
            x1, y1 = tr.transform_values(x0, y0, tr.scaling, kx, ky)
            line.set_xdata(x1)
            line.set_ydata(y1)
        
        fig.canvas.draw_idle()

    # Method to update the line of reflection when the reflection sliders values are altered
    def update_reflection_line(val) -> None:    
        warnings.filterwarnings("ignore", category=RuntimeWarning) # Supress division by 0 warnings when computing gradient for vertical line 
        x_component, y_component = reflection_x_slider.val, reflection_y_slider.val
        gradient = y_component/x_component
        f = lambda x: gradient*x
        y = f(x)
        reflection_line.set_ydata(y)
       
    
    # Method to perform reflection when the reflection button is clicked 
    def update_reflection(val) -> None:
        x_component, y_component = reflection_x_slider.val, reflection_y_slider.val
        for line in selected_lines:
            index = lines.index(line)
            x0, y0 = current_data[index]
            x1, y1 = tr.transform_values(x0, y0, tr.reflection, Vector([x_component,y_component]))
            current_data[index] = (x1, y1) # next rotation should be based of previous one as a button is being used instead of just the sliders alone 
            line.set_xdata(x1)
            line.set_ydata(y1)
        
        fig.canvas.draw_idle()
    
    # Method to deal with change in the translation sliders
    def update_translation(val) -> None:
        x_component, y_component = translation_x_slider.val, translation_y_slider.val
        for line in selected_lines:
            index = lines.index(line)
            x0, y0 = current_data[index]
            x1, y1 = tr.transform_values(x0, y0, tr.translation, Vector([x_component, y_component]))
            line.set_xdata(x1)
            line.set_ydata(y1)
        
        fig.canvas.draw_idle()


    # Method to change the sliders based on what transformation is selected 
    def transformation_selection(label) -> None:
        for index, line in enumerate(lines):
            current_data[index] = (line.get_xdata(), line.get_ydata())
        
        for widget in current_widgets:
            if isinstance(widget, Slider):
                widget.reset()

        hide_widgets(current_widgets)
        current_widgets.clear()

        ax_reset_button.set_position(INITIAL_RESET_SLIDER_POS)

        match label:
            case "Rotation":
                rotation_center_point.set_visible(True)
                reflection_line.set_visible(False)
                current_widgets.extend([rotation_slider, rotation_center_x_slider, rotation_center_y_slider])
            case "Shearing":
                rotation_center_point.set_visible(False)
                reflection_line.set_visible(False)
                current_widgets.extend([shearing_kx_slider, shearing_ky_slider])
            case "Scaling": 
                rotation_center_point.set_visible(False)
                reflection_line.set_visible(False)
                current_widgets.extend([scaling_kx_slider, scaling_ky_slider])
            case "Reflection":
                ax_reset_button.set_position([0.85, 0.05, 0.1, 0.1])
                rotation_center_point.set_visible(False)
                reflection_line.set_visible(True)
                current_widgets.extend([reflection_x_slider, reflection_y_slider, reflection_button])
            case _:
                rotation_center_point.set_visible(False)
                reflection_line.set_visible(False)
                current_widgets.extend([translation_x_slider, translation_y_slider])

        show_widgets(current_widgets)
        fig.canvas.draw_idle()

    # Method to deal with changes to functions being selected 
    def toggle_plot(label) -> None:
        index = func_labels.index(label) # Finds the index of the label within func_labels
        line = lines[index] # Finds the corresponding plot/line which matches the label

        if line in selected_lines:
            selected_lines.remove(line) # Remove line as it is being toggled off
            line.set_alpha(0.3) # Set non selected line to transparent 
        else:
            selected_lines.append(line) # Add line as it is being toggled on
            line.set_alpha(1.0) # Set selected line to opaque

        fig.canvas.draw_idle()

    # Function to place a point at a given position in the graph and display the coordinates of it
    def on_click_place_point(event) -> None:
        if event.inaxes is not None and event.key == "control" and event.button == 1:
            x_pos, y_pos = event.xdata, event.ydata
            xlim, ylim = ax.get_xlim(), ax.get_ylim()
            x_diff, y_diff = xlim[1] - xlim[0], ylim[1] - ylim[0]
            point, = ax.plot(x_pos, y_pos, 'ro')
            text = ax.text(x_pos+(x_diff*SCALE_POINT_X), y_pos+(y_diff*SCALE_POINT_Y), f'({x_pos:.2f}, {y_pos:.2f})', fontsize=8, ha='center', va='bottom', color='red', bbox=dict(facecolor='white', alpha=0.5))
            points.append((point, text))

            fig.canvas.draw_idle()
    
    # Function to remove a point from the graph 
    def on_click_remove_point(event) -> None:
        if event.inaxes is not None and event.key == "control" and event.button == 3:
            x_pos, y_pos = event.xdata, event.ydata
            xlim, ylim = ax.get_xlim(), ax.get_ylim()
            x_diff, y_diff = xlim[1] - xlim[0], ylim[1] - ylim[0] 
            new_points = []
            for point, text in points:
                point_size = point.get_markersize()
                fig_width, fig_height = fig.get_size_inches()
                ax_width = fig_width * ax.get_position().width
                ax_height = fig_height * ax.get_position().height
                point_size_x = (point_size*POINT_INCH_SCALE)*(x_diff/ax_width)
                point_size_y = (point_size*POINT_INCH_SCALE)*(y_diff/ax_height)
                x_point, y_point = point.get_xdata(), point.get_ydata()
                x_bound = abs(x_pos-x_point) <= point_size_x/2
                y_bound = abs(y_pos-y_point) <= point_size_y/2
                if x_bound and y_bound:
                    point.remove()
                    text.remove()
                else:  
                    new_points.append((point, text))
            
            points[:] = new_points
            fig.canvas.draw_idle()
            

    # Function to update the position of the coordinates text box with respect to the zoom of the plot
    def update_textbox_position(event) -> None:
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        x_diff = xlim[1] - xlim[0]
        y_diff = ylim[1] - ylim[0]
        for point, text in points:
            x_point, y_point = point.get_xdata(), point.get_ydata()
            if (xlim[0] <= x_point <= xlim[1]) and (ylim[0] <= y_point <= ylim[1]):
                new_x = point.get_xdata()+(x_diff*SCALE_POINT_X)  
                new_y = point.get_ydata()+(y_diff*SCALE_POINT_Y)
                text.set_x(new_x)
                text.set_y(new_y)
                text.set_visible(True)
            else:
                text.set_visible(False)  

        fig.canvas.draw_idle()

    # Method to reset any changes to the plot and sliders
    def reset_plot(label) -> None:
        for widget in current_widgets:
            if isinstance(widget, Slider):
                widget.reset()

        for line in selected_lines:
            index = lines.index(line)
            current_data[index] = initial_data[index]
            line.set_xdata(initial_data[index][0])
            line.set_ydata(initial_data[index][1])

        fig.canvas.draw_idle()

    # Calls the handler functions when an event occurs 
    # Rotation handlers
    rotation_slider.on_changed(update_rotation)
    rotation_center_x_slider.on_changed(update_rotation)
    rotation_center_y_slider.on_changed(update_rotation)
    # Shearing handlers
    shearing_kx_slider.on_changed(update_shearing)
    shearing_ky_slider.on_changed(update_shearing)
    # Scaling handlers
    scaling_kx_slider.on_changed(update_scaling)
    scaling_ky_slider.on_changed(update_scaling)
    # Reflection handlers
    reflection_x_slider.on_changed(update_reflection_line)
    reflection_y_slider.on_changed(update_reflection_line)
    reflection_button.on_clicked(update_reflection)
    # Translation handlers
    translation_x_slider.on_changed(update_translation)
    translation_y_slider.on_changed(update_translation)
    # Transformation selector handler
    transformation_selector.on_clicked(transformation_selection)
    # Function selector handler
    function_selector.on_clicked(toggle_plot)
    # Reset button handler
    reset_button.on_clicked(reset_plot)
    # Mouse click even handler
    fig.canvas.mpl_connect('button_press_event', on_click_place_point)
    fig.canvas.mpl_connect('button_press_event', on_click_remove_point)
    ax.callbacks.connect('xlim_changed', update_textbox_position)
    ax.callbacks.connect('ylim_changed', update_textbox_position)

    plt.show()

# Running the main function
visualiser_main()
