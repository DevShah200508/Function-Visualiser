import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import sys
from vector import Vector
from matrix import Matrix
from colorama import Fore, Style
from custom import custom_is_constant, custom_function_filter
from time import sleep
from matplotlib.widgets import Slider
from random import uniform


PI = np.pi

# Function to translate a vector to another vector
def translation(v: Vector, u: Vector) -> Vector:
    return v.add(u)

# Function to project a vector onto another vector
def projection(v: Vector, u: Vector) -> Vector:
    u_Matrix = u.toMatrix()
    v_Matrix = v.toMatrix()
    projection_Matrix = u_Matrix.multiply(u_Matrix.transpose()).scale(1/u.dotProduct(u))
    projected_Vector = projection_Matrix.multiply(v_Matrix).toVector()
    return projected_Vector

# Function to shear a vector by some scale factors kx and ky
def shearing(v: Vector, kx: float, ky:float) -> Vector:
    shearing_Matrix = Matrix((2,2), [[1, kx]
                                    ,[ky, 1]])
    v_Matrix = v.toMatrix()
    sheared_Vector = shearing_Matrix.multiply(v_Matrix).toVector()
    return sheared_Vector

# Function to scale a vector by some scale factors kx and ky
def scaling(v: Vector, kx: float, ky: float) -> Vector:
    scaling_Matrix = Matrix((2,2), [[kx, 0]
                                   ,[0, ky]])
    v_Matrix = v.toMatrix()
    scaled_Vector = scaling_Matrix.multiply(v_Matrix).toVector()
    return scaled_Vector

# Function to reflect a vector in a given axis
def reflection(v: Vector, axis: str) -> Vector:
    if (axis == "x"):
        reflection_Matrix = Matrix((2,2), [[1, 0]
                                        ,[0, -1]])
    elif (axis == "y"):
        reflection_Matrix = Matrix((2,2), [[-1, 0]
                                        ,[0, 1]])
    else:
        raise ValueError(Fore.RED + 'Make sure to choose either "x" for x axis or "y" for y axis!' + Style.RESET_ALL)
    v_Matrix = v.toMatrix()
    reflected_Vector = reflection_Matrix.multiply(v_Matrix).toVector()
    return reflected_Vector

# Function to rotate a vector about a given point, with a given angle, in a given direction
def rotation(v: Vector, u: Vector, θ: float) -> Vector:
    rotation_Matrix = Matrix((2,2), [[np.cos(θ), np.sin(θ)]
                                    ,[-np.sin(θ), np.cos(θ)]])
    transformed_v = v.add(u.scale(-1))
    transformed_v_Matrix = transformed_v.toMatrix()
    rotated_Vector = rotation_Matrix.multiply(transformed_v_Matrix).toVector().add(u)
    return rotated_Vector

# Method to retrieve function from user input. Constant k for k functions. Colors are chosen randomly 
def get_function(k: int, labels=[]):
    funcs = []
    print("Input a function in terms of x (no constants!), (Use (* /) for multiplication/division, (+ -) for addition and subtraction and (**) for powers, exp(x) for e^x)")
    sleep(2)
    for i in range(k):
        while True:
            u_input = input(f"f{i}(x) = ")
            try:
                func = sp.sympify(u_input)

                if (isinstance(func, sp.Symbol) and u_input != "x") or custom_is_constant(u_input):
                    raise sp.SympifyError(f"'{u_input}' is not a valid mathematical expression.")
                
                x = sp.symbols("x")
                labels.append(f"f{i}(x) = {str(func)}")
                funcs.append(sp.lambdify(x, func, 'numpy'))
                break
            except sp.SympifyError:
                print(Fore.LIGHTMAGENTA_EX + 'Invalid form of function, make sure function is valid and all variables are denoted with the letter "x" and no constants are inputted! Try again...' + Style.RESET_ALL)
                sleep(2)
    return funcs, labels

# Method to retrieve the number of functions being plotted from user input
def get_function_numbers() -> int:
    while True:
        try:
            k = int(input("Please input the number of functions you want to plot: "))
            if (k < 0):
                raise TypeError
            return k
        except TypeError:
            print(Fore.LIGHTMAGENTA_EX + 'Make sure you input a positive whole number!' + Style.RESET_ALL)
            sleep(2.0)

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
        except (TypeError, ValueError):
            print(Fore.LIGHTMAGENTA_EX + 'Make sure you input a whole number and chose a valid range!' + Style.RESET_ALL)



# Helper function to transform_function to help perform transformations depending on the type of transformation
def transform_values(x, y, t, *args):
    x_transformed, y_transformed = [], []
    for xi, yi in zip(x, y):
        v_projected = t(Vector(2, [xi, yi]), *args)
        x_transformed.append(v_projected.values[0])
        y_transformed.append(v_projected.values[1])
    return x_transformed, y_transformed

# Function to transform a function by linear transformations e.g translation, shearing, scaling, reflection and rotation
def transform_function(f, x: list[float]) -> tuple[list[float], list[float]]:
    y = f(x)
    while True:
        t = input("Input a transformation out of 'translation', 'shearing', 'scaling', 'reflection', 'rotation' or you can quit by typing 'exit': ")
        match t.lower().strip():
            case "translation":
                while True:
                    try:
                        u = Vector(2, [float(x) for x in input("Input 2 components (separated by spaces) of the vector you want to translate function by: ").split()])
                        return transform_values(x, y, translation, u)
                    except ValueError:
                        print(Fore.LIGHTMAGENTA_EX + "Make sure to type in exactly 2 components (separated by spaces), ensuring both are real numbers. Try again..." + Style.RESET_ALL)
                        sleep(2)
            case "shearing":
                while True:
                    try:
                        kx, ky = [float(x) for x in input("Input 2 scalars (separated by spaces) kx then ky: ").split()]
                        return transform_values(x, y, shearing, kx, ky)
                    except ValueError:
                        print(Fore.LIGHTMAGENTA_EX + "Make sure to type in exactly 2 values (separated by spaces), ensuring both are real numbers. Try again..." + Style.RESET_ALL)
                        sleep(2)
            case "scaling":
                while True:
                    try:
                        kx, ky = [float(x) for x in input("Input 2 scalars (separated by spaces) kx then ky: ").split()]
                        return transform_values(x, y, scaling, kx, ky)
                    except ValueError:
                        print(Fore.LIGHTMAGENTA_EX + "Make sure to type in exactly 2 values (separated by spaces), ensuring both are real numbers. Try again..." + Style.RESET_ALL)
                        sleep(2)
            case "reflection":
                while True:
                    try:
                        axis = input("Input an axis to reflect function in (either x or y): ")
                        return transform_values(x, y, reflection, axis)
                    except ValueError:
                        print(Fore.LIGHTMAGENTA_EX + "Make sure to type in either x or y for axis. Try again..." + Style.RESET_ALL)
                        sleep(2)
            case "rotation":
                while True:
                    try:
                        angle = float(input("Input the angle you want to rotate by: "))
                        u = Vector(2, [float(x) for x in input("Input 2 components (separated by spaces) of the point you want to rotate about : ").split()])
                        return transform_values(x, y, rotation, u, angle * PI/180)
                    except ValueError:
                        print(Fore.LIGHTMAGENTA_EX + "Make sure to input real number for angle. Ensure coordinates are typed properly. Try again..." + Style.RESET_ALL)
                        sleep(2)
            case "exit":
                sys.exit()
            case _:
                print(Fore.LIGHTMAGENTA_EX + "Make sure to input a valid transformation! Try again..." + Style.RESET_ALL)
                sleep(2)


# Method to plot functions for visual representation
def plot_functions(x_arr: list[list[float]], y_arr: list[list[float]], colors: tuple, labels=None) -> None:
    if (len(colors) != len(y_arr)):
        raise ValueError(Fore.RED + "Make sure to input a color for all the functions!" + Style.RESET_ALL)
    try:
        for i, (x, y, color) in enumerate(zip(x_arr, y_arr, colors)):
            plt.plot(x, y, label=labels[i] if labels else None, color=color)
    except ValueError:
        print(Fore.RED + "Invalid colour input, please input correct colours!" + Style.RESET_ALL)
        raise
    plt.rcParams["font.size"] = 7.5
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axhline(0, color='black',linewidth=1.5)
    plt.axvline(0, color='black',linewidth=1.5)
    plt.title('Plot of functions')
    plt.grid(True)
    plt.legend()
    plt.show()

    # Method to plot vectors for visual representation
def plot_vectors(vectors: list[Vector], colors: list[str], labels=None) -> None:
    if (len(colors) != len(vectors)):
        raise ValueError(Fore.RED + "Make sure to input a color for all the vectors!" + Style.RESET_ALL)
    try:
        for i, (vector, color) in enumerate(zip(vectors, colors)):
            plt.quiver(0, 0, vector.values[0], vector.values[1], angles="xy", scale_units="xy", scale=0.5, color=color, label = labels[i] if labels else None)
    except ValueError:
        print(Fore.RED + "Invalid colour input, please input correct colour!" + Style.RESET_ALL)
    plt.rcParams["font.size"] = 7.5
    plt.xlim(-15, 15)
    plt.ylim(-15, 15)
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.title("Linear transformation")
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.show()

# Main function
def main():
    k = get_function_numbers()
    f_arr, labels = get_function(k)
    min_x, max_x, min_y, max_y = get_axis_lim()
    x_arr, y_arr, colors = [], [], []
    x = np.linspace(min_x, max_x, num=(max_x-min_x)*10)
    for i, f in enumerate(f_arr):
        x_filtered, y_filtered = custom_function_filter(x, f(x), min_x, max_x, min_y, max_y)
        x_arr.append(x_filtered)
        y_arr.append(y_filtered) 
        colors.append(get_random_color())
        x_transformed, y_transformed = custom_function_filter(*transform_function(f, x), min_x, max_x, min_y, max_y)
        x_arr.append(x_transformed)
        y_arr.append(y_transformed)
        colors.append(get_random_color())
        labels.append(f"transformed f{i}(x)")
    plot_functions(x_arr, y_arr, colors=colors, labels=labels)

    #plot_vectors(vector_color_pairs, labels=["v1", "v2", "v1_transformed", "v2_transformed"])

if __name__ == "__main__":
    main()