import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("300x400")
        
        # Variable to store current expression
        self.expression = ""
        self.input_text = tk.StringVar()

        # Entry field (Display)
        input_frame = self.create_display()
        input_frame.pack(side=tk.TOP)

        # Buttons
        btns_frame = self.create_buttons()
        btns_frame.pack()

    def create_display(self):
        frame = tk.Frame(self.root, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        entry = tk.Entry(frame, font=('arial', 18, 'bold'), textvariable=self.input_text, width=50, bg="#eee", bd=0, justify=tk.RIGHT)
        entry.grid(row=0, column=0)
        entry.pack(ipady=10) # internal padding to increase height of input field
        return frame

    def create_buttons(self):
        frame = tk.Frame(self.root, width=312, height=322.5, bg="grey")
        
        # Button Layout
        # Row 1
        self.make_button(frame, "C", 1, 0, 3, lambda: self.btn_clear())
        self.make_button(frame, "/", 1, 3, 1, lambda: self.btn_click("/"))
        
        # Row 2
        self.make_button(frame, "7", 2, 0, 1, lambda: self.btn_click(7))
        self.make_button(frame, "8", 2, 1, 1, lambda: self.btn_click(8))
        self.make_button(frame, "9", 2, 2, 1, lambda: self.btn_click(9))
        self.make_button(frame, "*", 2, 3, 1, lambda: self.btn_click("*"))
        
        # Row 3
        self.make_button(frame, "4", 3, 0, 1, lambda: self.btn_click(4))
        self.make_button(frame, "5", 3, 1, 1, lambda: self.btn_click(5))
        self.make_button(frame, "6", 3, 2, 1, lambda: self.btn_click(6))
        self.make_button(frame, "-", 3, 3, 1, lambda: self.btn_click("-"))
        
        # Row 4
        self.make_button(frame, "1", 4, 0, 1, lambda: self.btn_click(1))
        self.make_button(frame, "2", 4, 1, 1, lambda: self.btn_click(2))
        self.make_button(frame, "3", 4, 2, 1, lambda: self.btn_click(3))
        self.make_button(frame, "+", 4, 3, 1, lambda: self.btn_click("+"))
        
        # Row 5
        self.make_button(frame, "0", 5, 0, 2, lambda: self.btn_click(0))
        self.make_button(frame, ".", 5, 2, 1, lambda: self.btn_click("."))
        self.make_button(frame, "=", 5, 3, 1, lambda: self.btn_equal())
        
        return frame

    def make_button(self, frame, text, row, col, colspan, command):
        tk.Button(frame, text=text, fg="black", width=10 * colspan, height=3, bd=0, bg="#fff", cursor="hand2", command=command).grid(row=row, column=col, padx=1, pady=1, sticky="nsew", columnspan=colspan)

        # Configure grid weights so buttons expand evenly
        frame.grid_columnconfigure(col, weight=1)
        frame.grid_rowconfigure(row, weight=1)

    def btn_click(self, item):
        self.expression = self.expression + str(item)
        self.input_text.set(self.expression)

    def btn_clear(self):
        self.expression = ""
        self.input_text.set("")

    def btn_equal(self):
        try:
            # eval is a built-in python function that evaluates a string as code
            result = str(eval(self.expression)) 
            self.input_text.set(result)
            self.expression = result # Allows chaining operations
        except ZeroDivisionError:
            self.input_text.set("Error")
            self.expression = ""
        except SyntaxError:
            self.input_text.set("Error")
            self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()