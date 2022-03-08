from tkinter import *
from tkinter import ttk
import tkinter as tk
from calculator import Calculator


# Constants for fonts
LABEL_FONT = ("Arial", 12)
DEFAULT_FONT = ("Arial", 10)


def call_Calculator():
    """Calls the Calculator module."""
    return Calculator()


class MyAgenda(object):
    """An application for organizing classwork."""

    def __init__(self):
        """Sets up the application."""
        # Main window initialization
        self.root = Tk()
        self.root.title("MyAgenda")
        self.root.iconbitmap('icon.ico')
        self.root.geometry("800x700")
        self.root.resizable(False, False)

        self.saveFile = []

        # Stylizes treeview widget and sets row height
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             font=LABEL_FONT)

        # Creates a frame to contain the notebook as well as the scrollbar for the notebook.
        self.tree_frame = Frame(self.root)
        self.tree_frame.grid(row=0, column=0, pady=20, columnspan=2, padx=20)
        self.tree_scroll = Scrollbar(self.tree_frame, width=25)
        self.tree_scroll.grid(row=0, column=2, sticky=NS)

        # Creates a treeview named 'notebook' that contains three columns named 'course,' 'chapter,' and 'task.'
        self.notebook = ttk.Treeview(self.tree_frame, height=20, yscrollcommand=self.tree_scroll.set)
        self.notebook['columns'] = ("Course", "Chapter", "Task")

        # Format the columns of 'notebook'
        self.notebook.column("#0", width=0,
                             stretch=NO)  # This line hides the default "invisible" column placed by treeview module
        self.notebook.column("Course", anchor=W, width=120)
        self.notebook.heading("Course", text="Course", anchor=W)
        self.notebook.column("Chapter", anchor=W, width=160)
        self.notebook.heading("Chapter", text="Chapter/Unit", anchor=W)
        self.notebook.column("Task", anchor=W, width=450)
        self.notebook.heading("Task", text="Task", anchor=W)

        # Attach 'notebook' to the grid of the main window.
        self.notebook.grid(row=0, column=0, columnspan=2)
        self.tree_scroll.config(command=self.notebook.yview)

        # Create the frames that contain buttons and input elements.
        self.input_frame = LabelFrame(self.root, text="Add New Task", padx=20, pady=10, font=LABEL_FONT)
        self.input_frame.grid(row=1, column=0, rowspan=2)
        self.input_fields = Frame(self.input_frame)
        self.input_fields.grid(row=0, column=0)
        self.input_buttons = Frame(self.input_frame)
        self.input_buttons.grid(row=1, column=0)
        self.other_buttons = LabelFrame(self.root, text="Other", padx=20, pady=10, font=LABEL_FONT)
        self.other_buttons.grid(row=1, column=1)

        # Create the elements to be contained within 'input_frame' and places them on their grid.
        self.course_label = Label(self.input_fields, text="Course", font=DEFAULT_FONT)
        self.course_label.grid(row=0, column=0)  # Course label and placement
        self.chapter_label = Label(self.input_fields, text="Chapter/Unit", font=DEFAULT_FONT)
        self.chapter_label.grid(row=0, column=1)  # Chapter label and placement
        self.course_input = Entry(self.input_fields, width=22, font=DEFAULT_FONT)
        self.course_input.grid(row=1, column=0, padx=10)  # Course entry field and placement
        self.chapter_input = Entry(self.input_fields, width=22, font=DEFAULT_FONT)
        self.chapter_input.grid(row=1, column=1, padx=10)  # Chapter entry field and placement
        self.task_label = Label(self.input_fields, text="Task", font=DEFAULT_FONT)
        self.task_label.grid(row=2, column=0, columnspan=2)  # Task label and placement
        self.task_input = Entry(self.input_fields, width=48, font=DEFAULT_FONT)
        self.task_input.grid(row=3, column=0, columnspan=2)  # Task entry field and placement

        self.add_task_button = Button(self.input_buttons, text="Add Task", padx=5, pady=10, font=DEFAULT_FONT,
                                      command=self.add_Task)
        self.add_task_button.grid(row=0, column=0, pady=20)  # Button that adds info to 'treeview'
        self.edit_button = Button(self.input_buttons, text="Overwrite Selected", font=DEFAULT_FONT,
                                  padx=5, pady=10,
                                  command=self.edit_Selected_Record)
        self.edit_button.grid(row=0, column=1)  # Button that replaces the selected record with current information
        self.clear_task_button = Button(self.input_buttons, text="Clear Fields", padx=10, pady=10, font=DEFAULT_FONT,
                                        command=self.clear_Fields)
        self.clear_task_button.grid(row=0, column=2, pady=20)  # Button that clears all fields

        # Creates the buttons to be contained within 'other_buttons' and places them on their grid.
        self.delete_button = Button(self.other_buttons, text="Delete Selected", font=DEFAULT_FONT,
                                    padx=40, pady=10,
                                    command=self.delete_Selected_Records)
        self.delete_button.grid(row=0, column=0, columnspan=2)
        self.call_calculator_button = Button(self.other_buttons, text="Calculator", font=DEFAULT_FONT,
                                             padx=10, pady=10,
                                             command=call_Calculator)
        self.call_calculator_button.grid(row=1, column=0)
        self.exit_program_button = Button(self.other_buttons, text="Exit Program", font=DEFAULT_FONT,
                                          padx=10, pady=10,
                                          command=self.root.destroy)
        self.exit_program_button.grid(row=1, column=1)

        # Test data that demonstrates to the user how records can be altered within 'notebook'
        self.notebook.insert(parent='', index='end', values=('History', 'Chapter 8', 'Study for test'))
        self.notebook.insert(parent='', index='end', values=('History', 'Chapter 9', 'Write out note cards'))
        self.notebook.insert(parent='', index='end', values=('Math', 'Unit 4', 'Homework - questions #6-20'))
        self.notebook.insert(parent='', index='end', values=('English Lit', 'Poetry', 'Work on Poe response'))

    def add_Task(self):
        """Adds the data in the input boxes to 'notebook'."""
        # Data validation happens at the beginning of the function to ensure that data exists in the
        # 'task' field to ensure that empty records are not created.
        while self.task_input.get() == "":
            return None

        # If the input is valid, then a record is created and the input boxes are cleared.
        self.notebook.insert(parent='', index='end',
                             values=(self.course_input.get(), self.chapter_input.get(), self.task_input.get()))
        self.clear_Fields()

        # The cursor is automatically placed in the 'course_input' field for the next record entry.
        self.course_input.focus_force()

    def clear_Fields(self):
        """Clears the input fields of their data."""
        self.course_input.delete(0, END)
        self.chapter_input.delete(0, END)
        self.task_input.delete(0, END)

    def edit_Selected_Record(self):
        """Overwrites the selected record with input data, or topmost selected record if
        multiple records are selected."""
        # Error handling for "Edit Selected" is clicked and no record is selected, which
        # will display an error message in the terminal.
        try:
            selected_item = self.notebook.selection()[0]
            self.notebook.item(selected_item,
                               values=(self.course_input.get(), self.chapter_input.get(), self.task_input.get()))
        except IndexError:
            pass

    def delete_Selected_Records(self):
        """Deletes the selected record(s) from 'notebook'."""
        x = self.notebook.selection()
        for record in x:
            self.notebook.delete(record)

    def run(self):
        """Runs the main loop."""
        self.root.mainloop()


# Entry point of the program
if __name__ == "__main__":
    agenda = MyAgenda()
    agenda.run()
