import matplotlib.pyplot as plt
import numpy as np
import transformation as t
from vector import Vector
from custom import custom_function_filter
from matplotlib.widgets import Slider, CheckButtons

def main():
    func_arr, func_labels = t.get_function(t.get_function_numbers()) # Retrieve all user inputted functions 
    min_x, max_x, min_y, max_y = t.get_axis_lim()
    value = 100
    x = np.linspace(-value, value, num=(value + value)*10)

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.3, bottom=0.35)
    lines = [] # Stores all functions/lines
    selected_lines = [] # Stores all the functions selected for transformation

    # Plotting the initial functions
    for i, f in enumerate(func_arr):
        x_filtered, y_filtered = x, f(x)
        line, = ax.plot(x_filtered, y_filtered, color=t.get_random_color(), label=func_labels[i]) # Unpack a single item tuple using ,
        lines.append(line) # Append the line object in the array of lines
        selected_lines.append(line) # Initially select all the lines
    
    plt.rcParams["font.size"] = 7.5
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(min(min_x, min_y), max(max_x, max_y))
    ax.set_ylim(min(min_x, min_y), max(max_x, max_y))
    ax.axhline(0, color='black',linewidth=1.5)
    ax.axvline(0, color='black',linewidth=1.5)
    ax.set_title('Plot of functions')
    ax.grid(True)
    ax.legend()

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

    rax = plt.axes([0.05, 0.4, 0.2, 0.2], facecolor='lightgoldenrodyellow')
    visibility = [True] * len(func_arr)
    function_selector = CheckButtons(rax, func_labels, visibility)

    # Method to deal with change in the rotation sliders
    def update_rotation(val):
        angle = rotation_slider.val
        center_x, center_y = rotation_center_x_slider.val, rotation_center_y_slider.val 
        for line in selected_lines:
            index = lines.index(line)
            f = func_arr[index]
            x_transformed, y_transformed = t.transform_values(x, f(x), t.rotation, Vector(2, [center_x, center_y]), angle * t.PI/180)
            line.set_xdata(x_transformed)
            line.set_ydata(y_transformed)
        
        fig.canvas.draw_idle()
    
    # Method to deal with changes to functions being selected 
    def toggle_plot(label):
        index = func_labels.index(label) # Finds the index of the label within func_labels
        line = lines[index] # Finds the corresponding plot/line which matches the label

        if line in selected_lines:
            selected_lines.remove(line) # Remove line as it is being toggled off
            line.set_alpha(0.1)
        else:
            selected_lines.append(line) # Add line as it is being toggled on
            line.set_alpha(1.0)

        fig.canvas.draw_idle()

    rotation_slider.on_changed(update_rotation)
    rotation_center_x_slider.on_changed(update_rotation)
    rotation_center_y_slider.on_changed(update_rotation)
    function_selector.on_clicked(toggle_plot)

    plt.show()

if __name__ == "__main__":
    main()