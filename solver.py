import math
import tkinter as tk


'''A Matrix-Vector calculator GUI '''

def main():
    root = tk.Tk()
    root.title("Linear equation solver")
    root.geometry("500x500")

    # Create a Label widget
    label = tk.Label(root, text="Hello, Tkinter!")
    label.pack()  # This adds the label to the window

    # Create a Button widget
    def on_button_click():
        label.config(text="Button Clicked!")

    button = tk.Button(root, text="Click Me", command=on_button_click)
    button.pack()  # This adds the button to the window

    root.mainloop()

if __name__ == "__main__":
    main()