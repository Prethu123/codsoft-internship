import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20)
        
        header_label = ttk.Label(header_frame, text="Password Generator", style='Header.TLabel')
        header_label.pack()
        
        # Length selection
        length_frame = ttk.Frame(self.root)
        length_frame.pack(pady=10)
        
        length_label = ttk.Label(length_frame, text="Password Length:")
        length_label.pack(side=tk.LEFT, padx=5)
        
        self.length_var = tk.IntVar(value=12)
        self.length_spinbox = ttk.Spinbox(length_frame, from_=6, to=30, width=5, textvariable=self.length_var)
        self.length_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Complexity options
        options_frame = ttk.Frame(self.root)
        options_frame.pack(pady=10)
        
        self.upper_var = tk.BooleanVar(value=True)
        upper_check = ttk.Checkbutton(options_frame, text="Uppercase Letters (A-Z)", variable=self.upper_var)
        upper_check.pack(anchor=tk.W, pady=2)
        
        self.lower_var = tk.BooleanVar(value=True)
        lower_check = ttk.Checkbutton(options_frame, text="Lowercase Letters (a-z)", variable=self.lower_var)
        lower_check.pack(anchor=tk.W, pady=2)
        
        self.digits_var = tk.BooleanVar(value=True)
        digits_check = ttk.Checkbutton(options_frame, text="Digits (0-9)", variable=self.digits_var)
        digits_check.pack(anchor=tk.W, pady=2)
        
        self.symbols_var = tk.BooleanVar(value=True)
        symbols_check = ttk.Checkbutton(options_frame, text="Symbols (!@#$%^&*)", variable=self.symbols_var)
        symbols_check.pack(anchor=tk.W, pady=2)
        
        # Generate button
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        generate_btn = ttk.Button(button_frame, text="Generate Password", command=self.generate_password)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        copy_btn = ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Password display
        display_frame = ttk.Frame(self.root)
        display_frame.pack(pady=10)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(display_frame, textvariable=self.password_var, width=40, font=('Arial', 12), justify=tk.CENTER)
        password_entry.pack(pady=5)
        
        # Strength indicator
        strength_frame = ttk.Frame(self.root)
        strength_frame.pack(pady=10)
        
        strength_label = ttk.Label(strength_frame, text="Password Strength:")
        strength_label.pack(side=tk.LEFT, padx=5)
        
        self.strength_var = tk.StringVar(value="")
        self.strength_indicator = ttk.Label(strength_frame, textvariable=self.strength_var, foreground="green")
        self.strength_indicator.pack(side=tk.LEFT, padx=5)
        
    def generate_password(self):
        # Check if at least one character set is selected
        if not any([self.upper_var.get(), self.lower_var.get(), self.digits_var.get(), self.symbols_var.get()]):
            messagebox.showerror("Error", "Please select at least one character type!")
            return
            
        # Define character sets
        upper_chars = string.ascii_uppercase if self.upper_var.get() else ""
        lower_chars = string.ascii_lowercase if self.lower_var.get() else ""
        digit_chars = string.digits if self.digits_var.get() else ""
        symbol_chars = "!@#$%^&*()" if self.symbols_var.get() else ""
        
        # Combine character sets
        all_chars = upper_chars + lower_chars + digit_chars + symbol_chars
        
        # Generate password
        length = self.length_var.get()
        password = ''.join(random.choice(all_chars) for _ in range(length))
        
        # Ensure at least one character from each selected set is included
        password_chars = list(password)
        random.shuffle(password_chars)
        password = ''.join(password_chars)
        
        self.password_var.set(password)
        self.evaluate_strength(password)
        
    def evaluate_strength(self, password):
        length = len(password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_digit = any(c in string.digits for c in password)
        has_symbol = any(c in "!@#$%^&*()" for c in password)
        
        score = 0
        if length >= 12: score += 2
        elif length >= 8: score += 1
        
        if has_upper: score += 1
        if has_lower: score += 1
        if has_digit: score += 1
        if has_symbol: score += 2
        
        if score >= 7:
            self.strength_var.set("Strong")
            self.strength_indicator.configure(foreground="green")
        elif score >= 4:
            self.strength_var.set("Medium")
            self.strength_indicator.configure(foreground="orange")
        else:
            self.strength_var.set("Weak")
            self.strength_indicator.configure(foreground="red")
            
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
