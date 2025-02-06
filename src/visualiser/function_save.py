import os
import csv

import numpy as np
import pandas as pd
from functools import wraps
from colorama import Fore, Style

"""
Store data in the form:

function_label | x data | y data |
"""
# Decorator function to enforce the filename to end with the '.csv' extension
def check_filename(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]
        f(*args, **kwargs)
        if not self.filename.endswith('.csv'):
            self.filename += '.csv'
    return wrapper

# Decorator function to check whether the inputted file location is valid
def check_location(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]
        f(*args, **kwargs)
        exists = os.path.exists(self.location)
        if not exists:
            print(f"Filepath {format(self.location)} does not exist")
    return wrapper

# Class to save function data into a csv file
class DataSaver:
    @check_location
    @check_filename
    def __init__(self, filename, location=None):
        self.filename = filename
        self.location = location if location is not None else os.getcwd() # default to the current working directory as the save location
        self.filePath = os.path.join(self.location, self.filename)
        self.header = ["function_label", "xdata", "ydata"]

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
            print("hello")
            with open(self.filePath, 'w', newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.header, delimiter=",")
                writer.writeheader()
                for datum in data:
                    datum["xdata"] = np.array2string(datum["xdata"], separator=',')
                    datum["ydata"] = np.array2string(datum["ydata"], separator=',')
                    writer.writerow(datum)
            print(Fore.LIGHTGREEN_EX + f"Data successfully saved in {self.filename}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error when trying to save data to {self.filename}\n Error: {e}" + Style.RESET_ALL)

    # Method to read data from a file
    def read(self) -> list[dict]:
        try:
            data = []
            with open(self.filePath, 'r', newline="") as file:
                reader = csv.DictReader(file, delimiter=",")
                for row in reader:
                    row["xdata"] = np.fromstring(row["xdata"].strip("[]"), sep=",")
                    row["ydata"] = np.fromstring(row["ydata"].strip("[]"), sep=",")
                    data.append(row)
            return data
        except Exception as e:
            print(Fore.RED + f"Error when trying to read the data from {self.filename}\n Error: {e}" + Style.RESET_ALL)

    @check_filename
    def set_filename(self, filename) -> None:
        self.filename = filename

    @check_location
    def set_location(self, location) -> None:
        self.location = location

def main() -> None:
    import numpy as np
    import ast
    x = np.linspace(0, 10, 100)
    y = (lambda k: np.sin(k))(x)
    data = [{"function_label":"sin(x)", "xdata":x, "ydata":y}]
    saver = DataSaver("test.csv")
    saver.save(data)
    dataOut = saver.read()
    print(dataOut[0]["xdata"][0])
    print(eval(data[0]["xdata"]))
    assert(np.allclose(dataOut[0]["xdata"], eval(data[0]["xdata"])))

if __name__ == "__main__":
    main()







