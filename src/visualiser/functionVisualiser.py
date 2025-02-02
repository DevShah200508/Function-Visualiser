import warnings
import matplotlib.pyplot as plt
import numpy as np
import functools
from matplotlib.widgets import Slider, CheckButtons, RadioButtons, Button
from src.transformations import transformation as tr
from src.transformations.vector import Vector
from src.custom import custom_get_random_color
from .input_handler import get_functions, get_axis_lim
from .widget_visibility_control import show_widgets, hide_widgets, transformation_line_visibility

warnings.filterwarnings("ignore", category=RuntimeWarning) # Supress division by 0 warnings when computing gradient for vertical line, and also warnings due to domain being out of function bound

# Constants that are used later within the script
PI = np.pi
RADIOBUTTON_LABELS = ["Rotation", "Shearing", "Scaling", "Reflection", "Translation"]
RESOLUTION = 0.1
TEXTBOX_TO_POINT_SCALE = 1/15
POINT_INCH_SCALE = 1/72
SLIDER_POS_1 = (0.1, 0.10, 0.65, 0.03)
SLIDER_POS_2 = (0.1, 0.15, 0.65, 0.03)
SLIDER_POS_3 = (0.1, 0.20, 0.65, 0.03)
TRANSFORMATION_SLIDER_POS = (0.85, 0.17, 0.1, 0.1)
RESET_SLIDER_POS = (0.85, 0.05, 0.1, 0.1)
HISTORY_SIZE = 5

# decorator function to update history
def update_history(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        data = {}
        self = args[0]
        if self.head+1 >= HISTORY_SIZE:
            self.history.pop(0)  # Remove the first element from the history
            self.history.append(None)  # Append empty slot for the new history
            self.head -= 1  # Move back the head by one to compensate for lost element
            self.read -= 1
        f(*args, **kwargs, data=data)
        self.read += 1
        self.head = self.read
        self.history[self.read] = data  # keep track of the previous positions of the functions before transformation
    return wrapper


class FunctionVisualiserApp:
    
    def __init__(self, window) -> None:
        # Storing the custom tkinter window 
        self.window = window

        # Variables for undo and redo functionality
        self.history = [None] * HISTORY_SIZE
        self.head = 0
        self.read = 0

        # The Figure
        self.fig = None
        self.ax = None

        # Storing all things to do with the line object and transformation themselves
        self.lines = [] # Stores all functions/lines and their corresponding transformation line (where the line will be after a transformation)
        self.selected_lines = [] # Stores all the functions selected for transformation and their corresponding transformation function (where the function will be after a tranformation)
        self.current_widgets = [] # Stores all the current widgets needing to be displayed on the screen
        self.initial_data = [] # Stores all the initial (x, y) state(s) of the graph, useful when resetting the graph
        self.current_data = None # This stores the current (x, y) data state of all the functions at any given time
        self.points = [] # Stores all the drawn markers/points
        self.rotation_center_point = None # Mark for the center point of rotation
        self.reflection_line = None # Line of reflection

        # Storing functions that need to be plotted and the bound on the axes
        self.func_arr = None # Array storing all the functions
        self.func_labels = None # Array storing all the function labels
        self.x = None # Initial set of x values 
        self.min_x = None # min value of x in the axes
        self.max_x = None # max value of x in the axes
        self.min_y = None # min value of y in the axes
        self.max_y = None # max value of y in the axes

        # All widgets
        self.rotation_slider = None
        self.rotation_center_x_slider = None
        self.rotation_center_y_slider = None
        self.shearing_kx_slider = None
        self.shearing_ky_slider = None
        self.scaling_kx_slider = None
        self.scaling_ky_slider = None
        self.reflection_slider = None
        self.translation_x_slider = None
        self.translation_y_slider = None
        self.transformation_selector = None
        self.function_selector = None
        self.transform_button = None
        self.reset_button = None

    def __setup_functions(self) -> None:
        self.func_arr, self.func_labels = get_functions(self.window) # Retrieve all user inputted functions 
        self.min_x, self.max_x, self.min_y, self.max_y = get_axis_lim(self.window) # Get the axis limits for the domain and range of the graph you want displayed 
        value = int(np.ceil(max(100+abs(self.max_x), 100+abs(self.min_x)))) # Ensures function is plotted out the visible view of the graph
        self.x = np.linspace(-value, value, num=int(value/RESOLUTION)) # Initial range values for x

    # Method for the setup of the initial plot
    def __setup_plots(self) -> None:
         # The figure
        self.fig, self.ax = plt.subplots() 
        # Plotting the initial functions
        for i, f in enumerate(self.func_arr):
            fx = f(self.x)
            self.initial_data.append((self.x, fx))
            color = custom_get_random_color() # Get a random colour for the plot
            line, = self.ax.plot(self.x, fx, color=color, label=self.func_labels[i]) # Unpack a single item tuple using ','
            transformation_line, = self.ax.plot(self.x, fx, color=color, alpha=0.30) # Transformation line to show the result of a transformation before it is actually done
            transformation_line.set_visible(False) # Initially set off the transformation line as it will overlap with the normal line
            self.lines.append((line, transformation_line))
            self.selected_lines.append((line, transformation_line))

        self.current_data = self.initial_data[:] # This stores the current (x, y) data state of all the functions at any given time
        self.history[self.head] = {key:val for key, val in enumerate(self.initial_data)} # Add the initial data to the history
        self.rotation_center_point, = self.ax.plot((self.min_x+self.max_x)/2, (self.min_y+self.max_y)/2, color="black", marker="x") # Mark for the center point of rotation
        self.reflection_line, = self.ax.plot(self.x, [0]*len(self.x), linestyle='--', color='grey', label='Line of reflection') # Line of reflection
        self.reflection_line.set_visible(False) # Initially set off the reflection line as the initial transformation will be rotation

        # Basic set up of the plot
        plt.subplots_adjust(left=0.3, bottom=0.35) # Create space for buttons and sliders
        plt.rcParams["font.size"] = 7.5
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_xlim(self.min_x, self.max_x)
        self.ax.set_ylim(self.min_y, self.max_y)
        self.ax.axhline(0, color='black',linewidth=1.5)
        self.ax.axvline(0, color='black',linewidth=1.5)
        self.ax.set_title('Plot of functions')
        self.ax.grid(True)
        self.ax.legend()
        self.fig.text(0.10, 0.95, "Function transformer", fontsize=20, fontweight='bold', ha="center", va="center")
        self.fig.text(0.13, 0.90, "• Use Ctrl + LMB to mark points and Ctrl + RMB to remove marked points from the axes.", fontsize=8, ha="center", va="center") 
        self.fig.text(0.13, 0.88, "• Toggle the function(s) you want to transform and select a transformation below.", fontsize=8, ha="center", va="center")
        self.fig.text(0.13, 0.86, "• Use the sliders to vary the parameters of the specified transformation.", fontsize=8, ha="center", va="center")

    # Method to create all the widgets that are going to be displayed on the screen
    def __setup_widgets(self) -> None:
        # Creation of initial sliders for all the neccessary transformations on a function
        ax_rotation_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
        self.rotation_slider = Slider(ax_rotation_slider, 'Rotation', -360, 360, valinit=0.0)

        ax_rotation_center_x_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
        self.rotation_center_x_slider = Slider(ax_rotation_center_x_slider, 'Rotation center (x)', self.min_x, self.max_x, valinit=(self.min_x+self.max_x)/2)

        ax_rotation_center_y_slider = plt.axes(SLIDER_POS_3, facecolor='lightgoldenrodyellow')
        self.rotation_center_y_slider = Slider(ax_rotation_center_y_slider, 'Rotation center (y)', self.min_y, self.max_y, valinit=(self.min_y+self.max_y)/2)
        
        # Set up the sliders for the shearing 
        ax_shearing_kx_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
        self.shearing_kx_slider = Slider(ax_shearing_kx_slider, 'kx shearing', -10, 10, valinit=0.0)

        ax_shearing_ky_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
        self.shearing_ky_slider = Slider(ax_shearing_ky_slider, 'ky shearing', -10, 10, valinit=0.0)

        # Set up the sliders for scaling 
        ax_scaling_kx_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
        self.scaling_kx_slider = Slider(ax_scaling_kx_slider, 'kx scaling', -10, 10, valinit=1.0)

        ax_scaling_ky_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
        self.scaling_ky_slider = Slider(ax_scaling_ky_slider, 'ky scaling', -10, 10, valinit=1.0)

        ax_reflection_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
        self.reflection_slider = Slider(ax_reflection_slider, 'reflection', 0, 180, valinit=0)

        # Set up the sliders for translation
        ax_translation_x_slider = plt.axes(SLIDER_POS_1, facecolor='lightgoldenrodyellow')
        self.translation_x_slider = Slider(ax_translation_x_slider, 'x translation', -abs(self.max_x-self.min_x), abs(self.max_x-self.min_x), valinit=0.0)

        ax_translation_y_slider = plt.axes(SLIDER_POS_2, facecolor='lightgoldenrodyellow')
        self.translation_y_slider = Slider(ax_translation_y_slider, 'y translation', -abs(self.max_y-self.min_y), abs(self.max_y-self.min_y), valinit=0.0)

        # Add the rotation sliders into the current sliders list as this will be the initial chosen transformation
        self.current_widgets.extend([self.rotation_slider, self.rotation_center_x_slider, self.rotation_center_y_slider])

        # Hide all the sliders which are not involved with rotation 
        hide_widgets([self.shearing_kx_slider, self.shearing_ky_slider, self.scaling_kx_slider, self.scaling_ky_slider, self.reflection_slider, self.translation_x_slider, self.translation_y_slider])

        # CheckButtons and RadioButtons for selecting function(s) and transformation(s)
        ax_transformation_selector = plt.axes((0.01, 0.35, 0.2, 0.2), facecolor='lightgreen')
        self.transformation_selector = RadioButtons(ax_transformation_selector, RADIOBUTTON_LABELS)

        ax_function_selector = plt.axes((0.01, 0.6, 0.2, 0.2), facecolor='lightgoldenrodyellow')
        visibility = [True] * len(self.func_arr)
        self.function_selector = CheckButtons(ax_function_selector, self.func_labels, visibility)
        
        # Button for performing (confirming) transformation
        ax_transform_button = plt.axes(TRANSFORMATION_SLIDER_POS, facecolor='lightblue')
        self.transform_button = Button(ax_transform_button, label="Transform!", hovercolor='dodgerblue')

        # Button for resetting any transformations to the plot 
        ax_reset_button = plt.axes(RESET_SLIDER_POS, facecolor='lightblue')
        self.reset_button = Button(ax_reset_button, label="Reset", hovercolor='dodgerblue')
    
    # Method for setting up the event handlers for the widgets
    def __setup_event_handlers(self) -> None:
        # Calls the handler functions when an event occurs 
        # Rotation handlers
        self.rotation_slider.on_changed(self.__update_rotation)
        self.rotation_center_x_slider.on_changed(self.__update_rotation)
        self.rotation_center_y_slider.on_changed(self.__update_rotation)
        # Shearing handlers
        self.shearing_kx_slider.on_changed(self.__update_shearing)
        self.shearing_ky_slider.on_changed(self.__update_shearing)
        # Scaling handlers
        self.scaling_kx_slider.on_changed(self.__update_scaling)
        self.scaling_ky_slider.on_changed(self.__update_scaling)
        # Reflection handler
        self.reflection_slider.on_changed(self.__update_reflection_line)
        # Translation handlers
        self.translation_x_slider.on_changed(self.__update_translation)
        self.translation_y_slider.on_changed(self.__update_translation)
        # Transformation selector handler
        self.transformation_selector.on_clicked(self.__transformation_selection)
        # Function selector handler
        self.function_selector.on_clicked(self.__toggle_plot)
        # Reset button handler
        self.reset_button.on_clicked(self.__reset_plot)
        # Transformation button handler
        self.transform_button.on_clicked(self.__perform_transformation)
        # Mouse click event handlers
        self.fig.canvas.mpl_connect('button_press_event', self.__on_click_place_point)
        self.fig.canvas.mpl_connect('button_press_event', self.__on_click_remove_point)
        self.fig.canvas.mpl_connect('key_press_event', self.__undo)
        self.fig.canvas.mpl_connect('key_press_event', self.__redo)
        self.ax.callbacks.connect('xlim_changed', self.__update_textbox_position)
        self.ax.callbacks.connect('ylim_changed', self.__update_textbox_position)

     # Method to deal with change in the rotation sliders
    def __update_rotation(self, _) -> None:    
        angle = self.rotation_slider.val
        center_x, center_y = self.rotation_center_x_slider.val, self.rotation_center_y_slider.val
        self.__update_rotation_center_point(center_x, center_y) # Update the position of the center point the axes
        self.__transform_plot(tr.rotation, Vector([center_x, center_y]), angle)
        self.fig.canvas.draw_idle()

    # Method to deal with change in the rotation_center sliders
    def __update_rotation_center_point(self, center_x: float, center_y: float) -> None:
        self.rotation_center_point.set_xdata([center_x])
        self.rotation_center_point.set_ydata([center_y])

    # Method to deal with change in the shearing sliders
    def __update_shearing(self, _) -> None:
        kx, ky = self.shearing_kx_slider.val, self.shearing_ky_slider.val
        self.__transform_plot(tr.shearing, kx, ky)
        self.fig.canvas.draw_idle()

    # Method to deal with change in the scaling sliders
    def __update_scaling(self, _) -> None:
        kx, ky = self.scaling_kx_slider.val, self.scaling_ky_slider.val
        self.__transform_plot(tr.scaling, kx, ky)
        self.fig.canvas.draw_idle()

    # Method to update the line of reflection when the reflection sliders values are altered
    def __update_reflection_line(self, _) -> None:     
        x_component, y_component = np.cos(self.reflection_slider.val*PI/180), np.sin(self.reflection_slider.val*PI/180)
        y = (lambda x: (y_component/x_component)*x)(self.x)
        self.reflection_line.set_ydata(y)
        self.__transform_plot(tr.reflection, Vector([x_component, y_component]))
        self.fig.canvas.draw_idle()

    # Method to deal with change in the translation sliders
    def __update_translation(self, _) -> None:
        x_component, y_component = self.translation_x_slider.val, self.translation_y_slider.val
        self.__transform_plot(tr.translation, Vector([x_component, y_component]))
        self.fig.canvas.draw_idle()

    # Method to transform line data based on a transformation and parameters
    def __transform_plot(self, transformation, *args) -> None:
        for line, transformation_line in self.selected_lines:
            transformation_line_visibility(line, transformation_line)
            index = self.lines.index((line, transformation_line))
            x0, y0 = self.current_data[index]
            x1, y1 = tr.transform_values(x0, y0, transformation, *args)
            transformation_line.set_xdata(x1)
            transformation_line.set_ydata(y1)

    # Perform the transformation, making the transformed function the new starting point
    @update_history
    def __perform_transformation(self, _,  data=None) -> None:
        if data is None:
            data = {}

        for index, (line, transformation_line) in enumerate(self.lines):
            x_transformed = transformation_line.get_xdata()
            y_transformed = transformation_line.get_ydata()
            data[index] = (x_transformed, y_transformed)
            line.set_xdata(x_transformed)
            line.set_ydata(y_transformed)
            self.current_data[index] = (x_transformed, y_transformed) # Set current line position as the current data

        self.__reset_widgets()
        self.fig.canvas.draw_idle()

        
    # Method to change the sliders based on what transformation is selected 
    def __transformation_selection(self, label) -> None:
        self.__reset_widgets()
        hide_widgets(self.current_widgets)
        self.current_widgets.clear()
        match label:
            case "Rotation":
               self.__transformation_selection_helper(True, False, self.rotation_slider, self.rotation_center_x_slider, self.rotation_center_y_slider)
            case "Shearing":
                self.__transformation_selection_helper(False, False, self.shearing_kx_slider, self.shearing_ky_slider)
            case "Scaling": 
                self.__transformation_selection_helper(False, False, self.scaling_kx_slider, self.scaling_ky_slider)
            case "Reflection":
                self.__transformation_selection_helper(False, True, self.reflection_slider)
            case _:
                self.__transformation_selection_helper(False, False, self.translation_x_slider, self.translation_y_slider)

        show_widgets(self.current_widgets)
        self.fig.canvas.draw_idle()
    
    def __transformation_selection_helper(self, rotation_center_visibility, reflection_line_visiblity, *args):
        print(len(args))
        self.rotation_center_point.set_visible(rotation_center_visibility)
        self.reflection_line.set_visible(reflection_line_visiblity)
        self.current_widgets.extend(list(args))
            
    # Method to deal with changes to functions being selected 
    def __toggle_plot(self, label) -> None:
        index = self.func_labels.index(label) # Finds the index of the label within func_labels
        line, transformation_line = self.lines[index] # Finds the corresponding plot/line which matches the label

        if (line, transformation_line) in self.selected_lines:
            self.selected_lines.remove((line, transformation_line)) # Remove line as it is being toggled off
            line.set_alpha(0.3) # Set non selected line to transparent
            transformation_line.set_visible(False) # Turn the transformation line off

        else:
            self.selected_lines.append((line, transformation_line)) # Add line as it is being toggled on
            line.set_alpha(1.0) # Set selected line to opaque
            transformation_line.set_visible(True)

        self.fig.canvas.draw_idle()

    # Method to allow undoing a transformation on a plot
    def __undo(self, event) -> None:
        if event.key == "ctrl+z":
                if self.read > 0:
                    self.read -= 1
                    self.set_data()
                print(f"head is {self.head} and read is {self.read}")

    # Method to allow redoing a transformation on a plot (if valid redo is available)
    def __redo(self, event) -> None:
        if event.key == "ctrl+y":
            if self.read < self.head:
                self.read += 1
                self.set_data()
            print(f"head is {self.head} and read is {self.read}")

    def set_data(self):
        data = self.history[self.read]
        for i, (line, transformation_line) in enumerate(self.lines):
            x0, y0 = data[i]
            line.set_xdata(x0)
            line.set_ydata(y0)
            transformation_line.set_xdata(x0)
            transformation_line.set_ydata(y0)
            self.current_data[i] = (x0, y0)

        self.__reset_widgets()
        self.fig.canvas.draw_idle()

    # Function to place a point at a given position in the graph and display the coordinates of it
    def __on_click_place_point(self, event) -> None:
        if event.inaxes is not None and event.key == "control" and event.button == 1:
            x_pos, y_pos = event.xdata, event.ydata
            xlim, ylim = self.ax.get_xlim(), self.ax.get_ylim()
            x_diff, y_diff = xlim[1] - xlim[0], ylim[1] - ylim[0]
            point, = self.ax.plot(x_pos, y_pos, 'ro')
            text = self.ax.text(x_pos+(x_diff*TEXTBOX_TO_POINT_SCALE), y_pos+(y_diff*TEXTBOX_TO_POINT_SCALE), f'({x_pos:.2f}, {y_pos:.2f})', fontsize=8, ha='center', va='bottom', color='red', bbox=dict(facecolor='white', alpha=0.5))
            self.points.append((point, text))

            self.fig.canvas.draw_idle()
    
    # Function to remove a point from the graph 
    def __on_click_remove_point(self, event) -> None:
        if event.inaxes is not None and event.key == "control" and event.button == 3:
            x_pos, y_pos = event.xdata, event.ydata
            xlim, ylim = self.ax.get_xlim(), self.ax.get_ylim()
            x_diff, y_diff = xlim[1] - xlim[0], ylim[1] - ylim[0] 
            new_points = []
            for point, text in self.points:
                point_size = point.get_markersize()
                fig_width, fig_height = self.fig.get_size_inches()
                ax_width = fig_width * self.ax.get_position().width
                ax_height = fig_height * self.ax.get_position().height
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
            
            self.points[:] = new_points
            self.fig.canvas.draw_idle()

    # Function to update the position of the coordinates text box with respect to the zoom of the plot
    def __update_textbox_position(self, _) -> None:
        xlim, ylim = self.ax.get_xlim(), self.ax.get_ylim()
        x_diff = xlim[1] - xlim[0]
        y_diff = ylim[1] - ylim[0]
        for point, text in self.points:
            x_point, y_point = point.get_xdata(), point.get_ydata()
            if (xlim[0] <= x_point <= xlim[1]) and (ylim[0] <= y_point <= ylim[1]):
                new_x = point.get_xdata()+(x_diff*TEXTBOX_TO_POINT_SCALE)  
                new_y = point.get_ydata()+(y_diff*TEXTBOX_TO_POINT_SCALE)
                text.set_x(new_x)
                text.set_y(new_y)
                text.set_visible(True)
            else:
                text.set_visible(False)  

        self.fig.canvas.draw_idle()

    # Method to reset any changes to the plot and sliders
    @update_history
    def __reset_plot(self, _, data=None) -> None:
        if data is None:
            data = {}

        for line, transformation_line in self.selected_lines:
            index = self.lines.index((line, transformation_line))
            self.current_data[index] = self.initial_data[index]
            x0, y0 = self.initial_data[index][0], self.initial_data[index][1]
            line.set_xdata(x0)
            line.set_ydata(y0)
            data[index] = (x0, y0)
            transformation_line.set_xdata(self.initial_data[index][0])
            transformation_line.set_ydata(self.initial_data[index][1])

        self.__reset_widgets()
        self.fig.canvas.draw_idle()

    # Method to reset all slider widgets
    def __reset_widgets(self) -> None:
        for widget in self.current_widgets:
            if isinstance(widget, Slider):
                widget.reset()


    # Method to run the app
    def run(self):
        try: # Try except blocks to deal with any issues that may arise with user input 
            self.__setup_functions() # set up the functions and the axes bounds
            self.__setup_plots() # Making the plots
            self.__setup_widgets() # Making the widgets
            self.__setup_event_handlers() # Linking to event handlers
            plt.show()
        except:
            print("Error!")
            return


