import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Calculator")
window.geometry("300x400")
window.configure(bg="#f0f0f0")

# Display widget
display = tk.Entry(window, font=('Arial', 20), justify='right', bd=5, relief=tk.SUNKEN)
display.insert(0, "0")
display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

# Store the current calculation
current_text = "0"
operation = None
first_number = 0

# Button click handler
def button_click(value):
    global current_text
    
    if current_text == "0" or current_text == "Error":
        current_text = ""
    
    current_text += str(value)
    display.delete(0, tk.END)
    display.insert(0, current_text)

# Operation handler
def operation_click(op):
    global current_text, operation, first_number
    
    try:
        first_number = float(current_text)
        operation = op
        current_text = "0"
        display.delete(0, tk.END)
        display.insert(0, "0")
    except:
        current_text = "Error"
        display.delete(0, tk.END)
        display.insert(0, "Error")

# Clear handler
def clear_click():
    global current_text, operation, first_number
    
    current_text = "0"
    operation = None
    first_number = 0
    display.delete(0, tk.END)
    display.insert(0, "0")

# Equals handler
def equals_click():
    global current_text, operation, first_number
    
    try:
        second_number = float(current_text)
        
        if operation == "+":
            result = first_number + second_number
        elif operation == "-":
            result = first_number - second_number
        elif operation == "*":
            result = first_number * second_number
        elif operation == "/":
            if second_number == 0:
                result = "Error"
            else:
                result = first_number / second_number
        else:
            result = current_text
            
        # Format the result
        if result == "Error":
            current_text = "Error"
        else:
            # If it's a whole number, display without decimal
            if result == int(result):
                result = int(result)
            current_text = str(result)
            
        display.delete(0, tk.END)
        display.insert(0, current_text)
        
        operation = None
        first_number = 0
        
    except:
        current_text = "Error"
        display.delete(0, tk.END)
        display.insert(0, "Error")

# Create buttons
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
    ('C', 5, 0)
]

# Add buttons to window
for (text, row, col) in buttons:
    if text == '=':
        btn = tk.Button(window, text=text, font=('Arial', 14), 
                       command=equals_click, bg="#4CAF50", fg="white")
    elif text == 'C':
        btn = tk.Button(window, text=text, font=('Arial', 14), 
                       command=clear_click, bg="#f44336", fg="white")
    else:
        if text in ['+', '-', '*', '/']:
            btn = tk.Button(window, text=text, font=('Arial', 14), 
                           command=lambda t=text: operation_click(t), bg="#FF9800")
        else:
            btn = tk.Button(window, text=text, font=('Arial', 14), 
                           command=lambda t=text: button_click(t), bg="#e0e0e0")
    
    btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
    btn.config(height=2, width=4)

# Configure grid weights
for i in range(6):
    window.grid_rowconfigure(i, weight=1)
for i in range(4):
    window.grid_columnconfigure(i, weight=1)

# Run the application
window.mainloop()
