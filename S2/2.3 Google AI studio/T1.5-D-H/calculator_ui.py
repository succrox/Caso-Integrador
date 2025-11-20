import tkinter as tk
from tkinter import messagebox

def on_click(event):
    text = event.widget.cget("text")
    
    if text == "=":
        try:
            expression = screen.get()
            result = eval(expression)
            screen.set(result)
        except Exception as e:
            screen.set("Error")
            messagebox.showerror("Error", "Invalid Input")
    elif text == "C":
        screen.set("")
    else:
        screen.set(screen.get() + text)

# --- GUI Setup ---
root = tk.Tk()
root.geometry("300x400")
root.title("Calculator")

screen = tk.StringVar()
entry = tk.Entry(root, textvar=screen, font="Arial 20 bold", justify="right")
entry.pack(fill="x", ipadx=8, pady=10, padx=10)

button_frame = tk.Frame(root)
button_frame.pack()

# Button Layout
buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "C", "0", "=", "+"
]

row_val = 0
col_val = 0

for button_text in buttons:
    btn = tk.Button(button_frame, text=button_text, font="Arial 15 bold", width=5, height=2)
    btn.grid(row=row_val, column=col_val, padx=5, pady=5)
    btn.bind("<Button-1>", on_click)

    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

root.mainloop()