import os
import csv
import numpy as np
from functools import wraps
from colorama import Fore, Style
from typing import Optional

"""
Store data in the form:

function_label | x data | y data |
"""

# Function to find the root of the project
def find_project_root(current_dir, marker) -> Optional[str]:
    while current_dir != os.path.dirname(current_dir):  # Keeps moving up until the root
        if marker in os.listdir(current_dir):
            return current_dir
        current_dir = os.path.dirname(current_dir)  # Go up one level
    return None  # Return None if marker is not found

# Decorator function to enforce the filename to end with the '.csv' extension
def check_filename(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]
        f(*args, **kwargs)
        if not self.filename.endswith('.csv'):
            self.filename += '.csv'
    return wrapper

# Class to save function data into a csv file
class DataSaver:
    @check_filename
    def __init__(self, filename):
        self.filename = filename
        self.location = find_project_root(os.getcwd(), marker="main.py") + "/save/" # default to the save folder in the root of the project as the save location
        self.filePath = os.path.join(self.location, self.filename)
        self.header = ["function_label", "xdata", "ydata", "bounds"]

    # Method to ensure data being saved is inputted in a valid format
    def __validate_data(self, data) -> None:
        for row in data:
            # Ensures data is in the form of dictionary
            if not isinstance(row, dict):
                raise ValueError("Data should be a list of dictionaries")
            # Ensures that data has been formatted correctly w.r.t the headers in the csv file
            if not all(key in row for key in self.header):
                raise ValueError(f"Each dictionary must have keys: {'|'.join(self.header)}")

    # Method to save the data
    def save(self, data) -> None:
        try:
            self.__validate_data(data)
            with open(self.filePath, 'w', newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.header, delimiter="|")
                writer.writeheader()
                for datum in data:
                    # Converty numpy array into string representation
                    xdata = np.array2string(datum["xdata"], separator=',')
                    ydata = np.array2string(datum["ydata"], separator=',')
                    bound = np.array2string(datum["bounds"], separator=',')
                    writer.writerow({self.header[0]:datum["function_label"], self.header[1]:xdata, self.header[2]:ydata, self.header[3]:bound})
            print(Fore.LIGHTGREEN_EX + f"Data successfully saved in {self.filename}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error when trying to save data to {self.filename}\n Error: {e}" + Style.RESET_ALL)

    # Method to read data from a file
    def read(self) -> list[dict]:
        try:
            data = []
            with open(self.filePath, 'r', newline="") as file:
                reader = csv.DictReader(file, delimiter="|")
                for row in reader:
                    row["xdata"] = np.fromstring(row["xdata"].strip("[]"), sep=",")
                    row["ydata"] = np.fromstring(row["ydata"].strip("[]"), sep=",")
                    if row["bounds"] != "N/A":
                        row["bounds"] = np.fromstring(row["bounds"].strip("[]"), sep=",")
                    data.append(row)
            return data
        except Exception as e:
            print(Fore.RED + f"Error when trying to read the data from {self.filename}\n Error: {e}" + Style.RESET_ALL)

    @check_filename
    def set_filename(self, filename) -> None:
        self.filename = filename


def main() -> None:
    import numpy as np
    x = np.linspace(0, 10, 100)
    y = (lambda k: np.sin(k))(x)
    bounds = np.array([-10,10,-10,10])
    data = [{"function_label":"sin(x)", "xdata":x, "ydata":y, "bounds":bounds}]
    saver = DataSaver("test.csv")
    saver.save(data)
    dataOut = saver.read()
    assert(np.allclose(dataOut[0]["xdata"], data[0]["xdata"]))

if __name__ == "__main__":
    main()







