import numpy as np
import matplotlib.pyplot as plt
from vector import Vector
from matrix import Matrix
from colorama import Fore, Style

# Store PI as a constant
PI = np.pi

# Function to translate a vector (v) by another vector (u)
def translation(v: Vector, u: Vector) -> Vector:
    return v.add(u)

# Function to project a vector (v) onto another vector (u)
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

# Function to reflect a vector in a given direction (u)
def reflection(v: Vector, u: Vector, axis: str) -> Vector:
    v_u_angle = u.angle(Vector(2, [1,0]))
    reflection_Matrix = Matrix((2,2), [[np.cos(2*v_u_angle), np.sin(v_u_angle)]
                                       ,[np.sin(2*v_u_angle), -np.cos(v_u_angle)]])
    v_Matrix = v.toMatrix()
    reflected_Vector = reflection_Matrix.multiply(v_Matrix).toVector()
    return reflected_Vector

# Function to rotate a vector about a given point (u) by an angle (θ)
def rotation(v: Vector, u: Vector, θ: float) -> Vector:
    rotation_Matrix = Matrix((2,2), [[np.cos(θ), np.sin(θ)]
                                    ,[-np.sin(θ), np.cos(θ)]])
    transformed_v = v.add(u.scale(-1))
    transformed_v_Matrix = transformed_v.toMatrix()
    rotated_Vector = rotation_Matrix.multiply(transformed_v_Matrix).toVector().add(u)
    return rotated_Vector

# Helper function to transform_function to help perform transformations depending on the type of transformation
def transform_values(x, y, t, *args):
    x_transformed, y_transformed = [], []
    for xi, yi in zip(x, y):
        v_projected = t(Vector(2, [xi, yi]), *args)
        x_transformed.append(v_projected.values[0])
        y_transformed.append(v_projected.values[1])
    return x_transformed, y_transformed

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
