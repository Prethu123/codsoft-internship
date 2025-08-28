import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Data file
        self.data_file = "todo_data.json"
        
        # Load tasks
        self.tasks = self.load_tasks()
        
        # Create GUI
        self.create_gui()
        
        # Populate tasks
        self.update_task_list()
    
    def create_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="To-Do List", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Task entry
        ttk.Label(main_frame, text="New Task:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.task_entry = ttk.Entry(main_frame, width=40)
        self.task_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Priority
        ttk.Label(main_frame, text="Priority:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.priority_var = tk.StringVar()
        priority_combo = ttk.Combobox(main_frame, textvariable=self.priority_var, 
                                     values=["Low", "Medium", "High"], state="readonly", width=10)
        priority_combo.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))
        priority_combo.set("Medium")
        
        # Due date
        ttk.Label(main_frame, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.due_date_entry = ttk.Entry(main_frame, width=15)
        self.due_date_entry.grid(row=3, column=1, sticky=tk.W, pady=(0, 5))
        
        # Add button
        add_btn = ttk.Button(main_frame, text="Add Task", command=self.add_task)
        add_btn.grid(row=4, column=1, sticky=tk.W, pady=(0, 10))
        
        # Task list frame
        list_frame = ttk.LabelFrame(main_frame, text="Tasks", padding="5")
        list_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Task list
        self.task_listbox = tk.Listbox(list_frame, height=15, selectmode=tk.SINGLE)
        self.task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for task list
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.task_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=(10, 0))
        
        # Action buttons
        complete_btn = ttk.Button(button_frame, text="Mark Complete", command=self.mark_complete)
        complete_btn.grid(row=0, column=0, padx=(0, 5))
        
        update_btn = ttk.Button(button_frame, text="Update Task", command=self.update_task)
        update_btn.grid(row=0, column=1, padx=5)
        
        delete_btn = ttk.Button(button_frame, text="Delete Task", command=self.delete_task)
        delete_btn.grid(row=0, column=2, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        clear_btn.grid(row=0, column=3, padx=(5, 0))
    
    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f)
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task.")
            return
        
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get().strip()
        
        # Validate date format if provided
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid date in YYYY-MM-DD format.")
                return
        
        task = {
            "id": len(self.tasks) + 1,
            "text": task_text,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.update_task_list()
        
        # Clear input fields
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.priority_var.set("Medium")
    
    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        
        for task in self.tasks:
            status = "✓" if task["completed"] else "☐"
            priority_symbol = {"Low": "⬇", "Medium": "➡", "High": "⬆"}[task["priority"]]
            
            display_text = f"{status} {priority_symbol} {task['text']}"
            if task["due_date"]:
                display_text += f" (Due: {task['due_date']})"
            
            self.task_listbox.insert(tk.END, display_text)
            
            # Color completed tasks differently
            if task["completed"]:
                self.task_listbox.itemconfig(tk.END, {'fg': 'gray'})
    
    def get_selected_task_index(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task.")
            return -1
        return selection[0]
    
    def mark_complete(self):
        index = self.get_selected_task_index()
        if index < 0:
            return
        
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_tasks()
        self.update_task_list()
    
    def update_task(self):
        index = self.get_selected_task_index()
        if index < 0:
            return
        
        # Create update window
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Task")
        update_window.geometry("400x200")
        update_window.resizable(False, False)
        
        # Center the update window
        update_window.transient(self.root)
        update_window.grab_set()
        
        # Task entry
        ttk.Label(update_window, text="Task:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        task_entry = ttk.Entry(update_window, width=30)
        task_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=(10, 5))
        task_entry.insert(0, self.tasks[index]["text"])
        
        # Priority
        ttk.Label(update_window, text="Priority:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        priority_var = tk.StringVar(value=self.tasks[index]["priority"])
        priority_combo = ttk.Combobox(update_window, textvariable=priority_var, 
                                     values=["Low", "Medium", "High"], state="readonly", width=10)
        priority_combo.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Due date
        ttk.Label(update_window, text="Due Date:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        due_date_entry = ttk.Entry(update_window, width=15)
        due_date_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        due_date_entry.insert(0, self.tasks[index]["due_date"])
        
        # Button frame
        button_frame = ttk.Frame(update_window)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def save_update():
            task_text = task_entry.get().strip()
            if not task_text:
                messagebox.showwarning("Warning", "Please enter a task.")
                return
            
            due_date = due_date_entry.get().strip()
            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showwarning("Warning", "Please enter a valid date in YYYY-MM-DD format.")
                    return
            
            self.tasks[index]["text"] = task_text
            self.tasks[index]["priority"] = priority_var.get()
            self.tasks[index]["due_date"] = due_date
            
            self.save_tasks()
            self.update_task_list()
            update_window.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_update).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=update_window.destroy).grid(row=0, column=1, padx=5)
    
    def delete_task(self):
        index = self.get_selected_task_index()
        if index < 0:
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            del self.tasks[index]
            self.save_tasks()
            self.update_task_list()
    
    def clear_all(self):
        if not self.tasks:
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
            self.tasks = []
            self.save_tasks()
            self.update_task_list()

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
