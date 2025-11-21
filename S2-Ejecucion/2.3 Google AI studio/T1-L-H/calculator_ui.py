import tkinter as tk
from tkinter import messagebox

def click_button(item):
    current_text = entry_field.get()
    entry_field.delete(0, tk.END)
    entry_field.insert(0, current_text + str(item))

def clear_field():
    entry_field.delete(0, tk.END)

def calculate():
    try:
        expression = entry_field.get()
        # eval() is a built-in Python function that evaluates a string as math
        result = eval(expression) 
        entry_field.delete(0, tk.END)
        entry_field.insert(0, str(result))
    except ZeroDivisionError:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, "Error")
    except Exception as e:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, "Error")

# --- Main Window Setup ---
root = tk.Tk()
root.title("Calculator")
root.geometry("300x400")
root.resizable(False, False)

# --- The Input Screen ---
entry_field = tk.Entry(root, width=16, font=("Arial", 24), borderwidth=5, relief="ridge", justify="right")
entry_field.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# --- Button Layout Configuration ---
# List of buttons: [Text, Row, Column]
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 3)
]

# Create Number and Operator Buttons
for (text, row, col) in buttons:
    tk.Button(root, text=text, width=5, height=2, font=("Arial", 14),
              command=lambda t=text: click_button(t)).grid(row=row, column=col, padx=5, pady=5)

# --- Special Buttons (Clear and Equal) ---
# These need specific styling or positions
btn_clear = tk.Button(root, text="C", width=5, height=2, font=("Arial", 14), bg="#ffcccc", command=clear_field)
btn_clear.grid(row=5, column=0, columnspan=2, sticky="we", padx=5, pady=5)

btn_equal = tk.Button(root, text="=", width=5, height=2, font=("Arial", 14), bg="#ccffcc", command=calculate)
btn_equal.grid(row=4, column=2, padx=5, pady=5)

# Run the app
root.mainloop()