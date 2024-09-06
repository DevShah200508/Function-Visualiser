import sys
import os 

# Insert the path to the src folder in the path variable 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from functionVisualiser import visualiser_main

# Delegates the main function to the main function in functionVisualiser.py
def main():
    visualiser_main()

if __name__ == "__main__":
    main()