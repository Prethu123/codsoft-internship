import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Game")
        self.root.geometry("500x600")
        self.root.configure(bg='#f0f8ff')
        
        # Initialize scores
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Rock Paper Scissors", 
                              font=('Arial', 24, 'bold'), fg='#2E86C1', bg='#f0f8ff')
        title_label.pack(pady=20)
        
        # Instructions
        instruction_label = tk.Label(self.root, text="Choose your weapon:", 
                                    font=('Arial', 14), bg='#f0f8ff')
        instruction_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#f0f8ff')
        button_frame.pack(pady=20)
        
        # Choice buttons
        self.rock_btn = tk.Button(button_frame, text="✊ Rock", font=('Arial', 14), 
                                 bg='#5DADE2', fg='white', width=10, height=2,
                                 command=lambda: self.play_game("rock"))
        self.rock_btn.grid(row=0, column=0, padx=10)
        
        self.paper_btn = tk.Button(button_frame, text="✋ Paper", font=('Arial', 14), 
                                  bg='#58D68D', fg='white', width=10, height=2,
                                  command=lambda: self.play_game("paper"))
        self.paper_btn.grid(row=0, column=1, padx=10)
        
        self.scissors_btn = tk.Button(button_frame, text="✌️ Scissors", font=('Arial', 14), 
                                     bg='#EC7063', fg='white', width=10, height=2,
                                     command=lambda: self.play_game("scissors"))
        self.scissors_btn.grid(row=0, column=2, padx=10)
        
        # Result display
        self.result_frame = tk.Frame(self.root, bg='#f0f8ff', relief=tk.GROOVE, bd=2)
        self.result_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        self.user_choice_label = tk.Label(self.result_frame, text="Your choice: ", 
                                         font=('Arial', 14), bg='#f0f8ff')
        self.user_choice_label.pack(pady=10)
        
        self.computer_choice_label = tk.Label(self.result_frame, text="Computer's choice: ", 
                                             font=('Arial', 14), bg='#f0f8ff')
        self.computer_choice_label.pack(pady=10)
        
        self.result_label = tk.Label(self.result_frame, text="Result: ", 
                                    font=('Arial', 16, 'bold'), bg='#f0f8ff')
        self.result_label.pack(pady=20)
        
        # Score display
        score_frame = tk.Frame(self.root, bg='#f0f8ff')
        score_frame.pack(pady=10)
        
        self.user_score_label = tk.Label(score_frame, text="Your Score: 0", 
                                        font=('Arial', 12), bg='#f0f8ff')
        self.user_score_label.grid(row=0, column=0, padx=20)
        
        self.ties_label = tk.Label(score_frame, text="Ties: 0", 
                                  font=('Arial', 12), bg='#f0f8ff')
        self.ties_label.grid(row=0, column=1, padx=20)
        
        self.computer_score_label = tk.Label(score_frame, text="Computer Score: 0", 
                                            font=('Arial', 12), bg='#f0f8ff')
        self.computer_score_label.grid(row=0, column=2, padx=20)
        
        # Play again button
        self.play_again_btn = tk.Button(self.root, text="Play Again", font=('Arial', 14), 
                                       bg='#F7DC6F', fg='black', width=15, height=1,
                                       command=self.reset_choices, state=tk.DISABLED)
        self.play_again_btn.pack(pady=20)
        
    def play_game(self, user_choice):
        # Disable choice buttons during result display
        self.rock_btn.config(state=tk.DISABLED)
        self.paper_btn.config(state=tk.DISABLED)
        self.scissors_btn.config(state=tk.DISABLED)
        
        # Get computer's choice
        computer_choice = random.choice(["rock", "paper", "scissors"])
        
        # Update choice displays
        self.user_choice_label.config(text=f"Your choice: {user_choice.capitalize()}")
        self.computer_choice_label.config(text=f"Computer's choice: {computer_choice.capitalize()}")
        
        # Determine winner
        if user_choice == computer_choice:
            result = "It's a tie!"
            self.ties += 1
            self.result_label.config(text=result, fg='#F39C12')
        elif (user_choice == "rock" and computer_choice == "scissors") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissors" and computer_choice == "paper"):
            result = "You win!"
            self.user_score += 1
            self.result_label.config(text=result, fg='#27AE60')
        else:
            result = "Computer wins!"
            self.computer_score += 1
            self.result_label.config(text=result, fg='#C0392B')
        
        # Update scores
        self.user_score_label.config(text=f"Your Score: {self.user_score}")
        self.ties_label.config(text=f"Ties: {self.ties}")
        self.computer_score_label.config(text=f"Computer Score: {self.computer_score}")
        
        # Enable play again button
        self.play_again_btn.config(state=tk.NORMAL)
    
    def reset_choices(self):
        # Reset the display
        self.user_choice_label.config(text="Your choice: ")
        self.computer_choice_label.config(text="Computer's choice: ")
        self.result_label.config(text="Result: ", fg='black')
        
        # Enable choice buttons
        self.rock_btn.config(state=tk.NORMAL)
        self.paper_btn.config(state=tk.NORMAL)
        self.scissors_btn.config(state=tk.NORMAL)
        
        # Disable play again button
        self.play_again_btn.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
