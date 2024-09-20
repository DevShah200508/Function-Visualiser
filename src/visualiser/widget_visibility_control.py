import numpy as np
from matplotlib import widgets
from matplotlib.lines import Line2D

# Method to hide widgets from the screen and deactivate them
def hide_widgets(widgets: widgets) -> None:
    for widget in widgets:
        widget.set_active(False)
        widget.ax.set_visible(False)       
          
# Method to show widgets on the screen and activate them
def show_widgets(widgets: widgets) -> None:
    for widget in widgets:
        widget.set_active(True)
        widget.ax.set_visible(True)  

# Method to turn off visibilty of the transformation_line if it overlaps over the main line
def transformation_line_visibility(line: Line2D, transformation_line: Line2D) -> None:
    x_line, y_line = line.get_xdata(), line.get_ydata()
    x_transformed_line, y_transformed_line = transformation_line.get_xdata(), transformation_line.get_ydata()
    if np.array_equal(x_line, x_transformed_line) and np.array_equal(y_line, y_transformed_line):
        transformation_line.set_visible(False)
    else:
        transformation_line.set_visible(True)
