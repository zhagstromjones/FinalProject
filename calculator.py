"""
Program: calculator.py
This is a basic calculator which evaluates expressions input
by the user and displays the results.
"""
import tkinter as tk

# Defines constants for font names and sizes
FONT_STYLE = ("Arial", 20)
DISPLAY_STYLE = ("Arial", 24)


class Calculator(object):
    def __init__(self):
        """Sets up the application."""
        self.window = tk.Tk()
        self.window.geometry("375x550")
        self.window.resizable(False, False)
        self.window.title("Calculator")
        self.window.iconbitmap("calcicon.ico")
        self.window.focus_force()

        # Sets the calculation display elements
        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        # Creates the output display
        self.label = self.create_display_label()

        # Places all ten digits in a dictionary. Keys are integers to be input to current_expression and
        # values are tuples that are used as grid coordinates.
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }

        # Places operations in a dictionary, using Unicode values for the divide and multiply symbols.
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        # This for-loop allows buttons to fill empty space evenly.
        self.buttons_frame = self.create_buttons_frame()
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        # Creates the buttons and binds their respective keyboard keys to them.
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_sqrt_button()
        self.create_square_button()
        self.bind_keys()

    def bind_keys(self):
        """Binds keys to their respective functions as defined by their dictionaries."""
        self.window.bind("<Return>", lambda event: self.evaluate())     # Press 'Enter' to evaluate the expression.
        self.window.bind("<Escape>", lambda event: self.clear())        # Press 'Esc' to clear the expression.
        for key in self.digits:     # A for-loop to bind keyboard digit keys to their respective digits.
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:  # A for-loop to bind keyboard operator keys to their respective operators.
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        """Creates the clear and equals buttons."""
        self.create_clear_button()  # Creates the 'clear' button
        self.create_equals_button()  # Creates the 'equals' button

    def create_display_label(self):
        """Creates and returns the current display as a label."""
        label = tk.Label(self.display_frame, text=self.current_expression,
                         font=DISPLAY_STYLE, anchor=tk.E, padx=24)
        label.pack(expand=True, fill="both")    # Creates and packs a label that will display the numbers.

        return label

    def create_display_frame(self):
        """Creates and returns the frame for the application."""
        frame = tk.Frame(self.window, height=221)
        frame.pack(expand=True, fill="both")    # Creates and packs a display frame for the numeric display.
        return frame

    def add_to_expression(self, value):
        """Adds the current value to the label."""
        self.current_expression += str(value)
        self.update_label()     # Updates the display label with the current expression.

    def create_digit_buttons(self):
        """Creates the buttons for the digits."""
        for digit, grid_value in self.digits.items():   # A for-loop to create the input buttons.
            button = tk.Button(self.buttons_frame, text=str(digit), font=FONT_STYLE,
                               command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        """Appends an operator to the end of the expression."""
        self.current_expression += operator                 # Adds the operator to 'current_expression'.
        self.total_expression += self.current_expression    # Adds 'current_expression' to 'total_expression'.
        self.current_expression = ""                        # Resets the current expression to an empty string.
        self.update_total_label()                           # Updates the total label.

    def create_operator_buttons(self):
        """Creates each operator button and appends their operators."""
        i = 0   # An accumulator used to place the operator button in the appropriate row.
        for operator, symbol in self.operations.items():    # A for-loop to place the operator buttons.
            button = tk.Button(self.buttons_frame, text=symbol, font=FONT_STYLE,
                               command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1  # Increase i to place button in the next row.

    def clear(self):
        """Clears both display labels."""
        self.current_expression = ""    # Resets 'current_expression' to an empty string.
        self.total_expression = ""      # Resets 'total_expression' to an empty string.
        self.update_label()             # Runs the 'update_label' function to limit the characters in the display.
        self.update_total_label()       # Runs the 'update_total_label' function to reset it.

    def create_clear_button(self):
        """Creates a button to clear both the total expression and current expression."""
        button = tk.Button(self.buttons_frame, text="C", font=FONT_STYLE, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        """Creates a square function."""
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        """Creates a square button."""
        button = tk.Button(self.buttons_frame, text="x\u00b2", font=FONT_STYLE, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        """Creates a square root function."""
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        """Creates the square root button."""
        button = tk.Button(self.buttons_frame, text="\u221ax", font=FONT_STYLE, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        """Evaluates the total expression label using the current expression."""
        self.total_expression += self.current_expression    # Adds 'current_expression' to 'total_expression'
        self.update_total_label()                           # Updates 'total_label'
        # The following is general-use error-handling in the event that an exception is thrown.
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        """Creates the '=' button."""
        button = tk.Button(self.buttons_frame, text="=", font=FONT_STYLE, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        """Creates and returns the frame that houses the buttons."""
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        """Updates the total_label based on the current expression."""
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f" {symbol} ")
        self.label.config(text=expression)

    def update_label(self):
        """Updates the current expression label, limiting display to 11 characters."""
        self.label.config(text=self.current_expression[:19])    # This limits the display to 19 characters.

    def run(self):
        """Runs the main loop."""
        self.window.mainloop()


# Entry point for the application
if __name__ == "__main__":
    calc = Calculator()
    calc.run()
