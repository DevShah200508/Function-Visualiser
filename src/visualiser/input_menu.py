import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from .functionVisualiser import FunctionVisualiserApp

# Constants
# Screen dimensions are stores as strings to allow tkinter to construct screen properly 
SCREEN_WIDTH = "1000" 
SCREEN_HEIGHT = "750"

# Set the initial theme of the GUI
ctk.set_appearance_mode("dark") # Setting appearance to dark
ctk.set_default_color_theme("green") # Setting colour theme to blue

class InputGUI(ctk.CTk):
    def __init__(self):
        super().__init__() # call the super class's constructor which is the ctk.CTk() method

        self.title("Function Visualiser")
        self.geometry("x".join([SCREEN_WIDTH, SCREEN_HEIGHT]))

        self.function_entries = []
        
        self.number_function_label = ctk.CTkLabel(self, text="Number of functions", text_color="#87D13C", font=(None, 20, "bold"), width=300)
        self.number_function_label.grid(row=0, column=0, padx=5, pady=5)

        self.function_number_entry = ctk.CTkEntry(self, placeholder_text="Enter between 1 to 8 functions:", font= (None, 15), width=300, height=50) 
        self.function_number_entry.grid(row=1, column=0, padx=5, pady=(0, 5))
        self.function_number_entry.bind("<Return>", self.update_function_number)

        self.function_label = ctk.CTkLabel(self, text="Functions", text_color="#87D13C", font=(None, 20, "bold"), width=300)
        self.function_label.grid(row=2, column=0, padx=5, pady=(5, 5))

        self.function_info_icon = ctk.CTkImage(Image.open("resources/icons/icons8-info-64.png"))

        self.function_info_button = ctk.CTkButton(self, text=" Info", text_color="#87D13C", image=self.function_info_icon, font=(None, 15, "bold"), fg_color="#242424", hover_color="#242424", border_width=2, border_color="#565b5e", width=100, anchor="w")
        self.function_info_button.grid(row=3, column=0)

        self.function_info_button.bind("<Enter>", self.button_hover_function_info_button)
        self.function_info_button.bind("<Leave>", self.off_button_hover_function_info_button)

        #self.function_info_label = ctk.CTkLabel(self, text="(*) Times, (/) division, (-) subtraction, (+) addition , (**) to the power", text_color="#87D13C", font=(None, 12, "bold"), width=290, wraplength=290)
        #self.function_info_label.grid(row=3, column=0, padx=5)

        self.function_frame = ctk.CTkFrame(self, width=290, height=384) 
        self.function_frame.grid(row=4, column=0, padx=5, pady=5)
        self.function_frame.grid_propagate(False)

        self.bound_label = ctk.CTkLabel(self, text="Graph bounds", text_color="#87D13C", font=(None, 20, "bold"), width=300)
        self.bound_label.grid(row=5, column=0, padx=5, pady=(5, 5))

        self.bound_frame = ctk.CTkFrame(self, width=290)
        self.bound_frame.grid(row=6, column=0, padx=5, pady=(0, 5))

        self.min_x_bound = ctk.CTkEntry(self.bound_frame, placeholder_text="x0:", width=60, height=20)
        self.min_x_bound.grid(row=0, column=0, padx=(10, 5), pady=3,)
        self.max_x_bound = ctk.CTkEntry(self.bound_frame, placeholder_text="x1:", width=60, height=20)
        self.max_x_bound.grid(row=0, column=1, padx=5, pady=3)
        self.min_y_bound = ctk.CTkEntry(self.bound_frame, placeholder_text="y0:", width=60, height=20)
        self.min_y_bound.grid(row=0, column=2, padx=5, pady=3)
        self.max_y_bound = ctk.CTkEntry(self.bound_frame, placeholder_text="y1:", width=60, height=20)
        self.max_y_bound.grid(row=0, column=3, padx=(5, 10), pady=3)

        self.plot_icon = ctk.CTkImage(Image.open("resources/icons/icons8-graph-64.png"))
        self.plot_button = ctk.CTkButton(self, text="Plot!", image=self.plot_icon, compound="left", font=(None, 17, "bold"), text_color="#87D13C", fg_color="#242424", hover_color="#242424", border_width=2, border_color="#565b5e", width=288, height=30, command=self.plot_functions)
        self.plot_button.grid(row=7, column=0, pady=(5,0))

        self.plot_button.bind("<Enter>", self.button_hover_plot_button)
        self.plot_button.bind("<Leave>", self.off_button_hover_plot_button)

        self.error_frame = ctk.CTkFrame(self, width=300, fg_color="#242424")
        self.error_frame.grid(row=8, column=0, pady=5)
        self.error_icon = ctk.CTkImage(Image.open("resources/icons/381599_error_icon.png")) 
        self.error_icon_label = ctk.CTkLabel(self.error_frame, text="")
        self.error_icon_label.grid(row=0, column=0, padx=(5, 0), pady=3)
        self.error_label = ctk.CTkLabel(self.error_frame, text="", compound="left", text_color="#fe2828", font=(None, 13, "bold"), width=240, height=25, wraplength=240)
        self.error_label.grid(row=0, column=0, padx=20, pady=(5, 0))

        self.level = self.winfo_toplevel()

        # Method to deal the with function_entry input when the submit button is pressed                              
    def update_function_number(self, event) -> None:
        self.destroy_widgets(self.function_entries) # Remove all the old function entries as new ones are going to be places
        self.function_entries.clear() # clear the array of function entries for new ones to be appended into the array
        user_input = self.function_number_entry.get() # retrieve the content of the entry box
        self.function_number_entry.delete(0, ctk.END) # Remove the entire entry from the function box
        try:            
            content = int(user_input)
            if (content < 1) or (content > 8):
                raise ValueError
            
        except ValueError:
                self.error_label.configure(text="   Make sure you input a whole number between 1 to 8!", image=self.error_icon)
                return
        
        self.error_label.configure(text="", image="") # If not errors are raised then remove the content in the error_label
        for i in range(content):
            entry = ctk.CTkEntry(self.function_frame, placeholder_text=f"f{i+1}:", width=280, text_color="#87D13C")
            entry.grid(row=i, column=0, padx=5, pady=10, sticky="W")
            self.function_entries.append(entry)

    # Method to process all inputted paramaters and plot an interactive plot of all the transformations 
    def plot_functions(self) -> None:
        functionVisualiser = FunctionVisualiserApp(self)
        functionVisualiser.run()


    def button_hover_function_info_button(self, event) -> None:
        self.function_info_button.configure(border_color="#87D13C")

    def off_button_hover_function_info_button(self, event) -> None:
        self.function_info_button.configure(border_color="#565b5e")

    def button_hover_plot_button(self, event) -> None:
        self.plot_button.configure(border_color="#87D13C")

    def off_button_hover_plot_button(self, event) -> None:
        self.plot_button.configure(border_color="#565b5e")

    def show_function_info(self) -> None:
        pass
         
    def destroy_widgets(self, widgets: list) -> None:
            for widget in widgets:
                widget.destroy()
        
    def run(self):
        self.mainloop()

def gui_main():
    app = InputGUI()
    app.run()

if __name__ == "__main__":
    main()