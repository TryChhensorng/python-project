import tkinter as tk
from tkinter import messagebox
import winsound  # For sound effects

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        
        # Initialize the game variables
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.players = ["X", "O"]
        self.current_player = 0
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_history = {"X": 0, "O": 0}
        
        # Game state variables
        self.game_started = False
        
        # Create the main UI elements
        self.create_main_ui()
    
    def create_main_ui(self):
        """Create the start, reset, and exit buttons, as well as the board."""
        
        # Instructions label
        self.instructions_label = tk.Label(self.root, text="Welcome to Tic Tac Toe!\nPlayer X starts the game.", font=('Arial', 14))
        self.instructions_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Create a grid of buttons for the board
        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(self.root, text=" ", width=10, height=3,
                                                   font=('Arial', 24), command=lambda r=row, c=col: self.on_button_click(r, c),
                                                   relief="raised", bd=5, bg="#f0f0f0")
                self.buttons[row][col].grid(row=row+1, column=col)
        
        # Create control buttons (Start, Reset, Exit)
        self.start_button = tk.Button(self.root, text="Start Game", width=15, height=2, font=('Arial', 12),
                                      command=self.start_game, relief="raised", bg="#4CAF50", fg="white")
        self.start_button.grid(row=4, column=0, pady=10)

        self.reset_button = tk.Button(self.root, text="Reset Game", width=15, height=2, font=('Arial', 12),
                                      command=self.reset_game, relief="raised", bg="#ff9800", fg="white")
        self.reset_button.grid(row=4, column=1, pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", width=15, height=2, font=('Arial', 12),
                                     command=self.root.quit, relief="raised", bg="#f44336", fg="white")
        self.exit_button.grid(row=4, column=2, pady=10)
        
        # Game history display
        self.history_label = tk.Label(self.root, text=f"Player X: {self.game_history['X']}  Player O: {self.game_history['O']}",
                                      font=('Arial', 14))
        self.history_label.grid(row=5, column=0, columnspan=3)

    def start_game(self):
        """Start a new game."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = 0
        self.update_buttons()
        self.instructions_label.config(text="Player X's turn.")
        self.game_started = True

    def update_buttons(self):
        """Update the board buttons."""
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ", bg="#f0f0f0")
    
    def on_button_click(self, row, col):
        """Handle the button click and update the game."""
        if not self.game_started:
            return
        
        if self.board[row][col] != " ":
            return  # Ignore clicks on already taken spots
        
        # Place the mark of the current player
        self.board[row][col] = self.players[self.current_player]
        self.buttons[row][col].config(text=self.players[self.current_player], bg="#e0e0e0")
        winsound.Beep(1000, 100)  # Play sound for move

        # Check for winner
        winner = self.check_winner()
        if winner:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            self.game_history[winner] += 1
            self.update_history()
            self.highlight_winner(winner)
            self.reset_game()
            return
        
        # Check for a draw
        if self.is_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()
            return
        
        # Switch player
        self.current_player = 1 - self.current_player
        self.instructions_label.config(text=f"Player {self.players[self.current_player]}'s turn.")
    
    def check_winner(self):
        """Check for a winner."""
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return self.board[i][0]
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return self.board[0][i]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]
        
        return None
    
    def is_draw(self):
        """Check if the game is a draw."""
        for row in self.board:
            if " " in row:
                return False
        return True
    
    def reset_game(self):
        """Reset the game for a new round."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = 0
        self.update_buttons()
        self.instructions_label.config(text="Game Reset. Click 'Start Game' to play.")
        self.game_started = False
    
    def update_history(self):
        """Update the score history."""
        self.history_label.config(text=f"Player X: {self.game_history['X']}  Player O: {self.game_history['O']}")
    
    def highlight_winner(self, winner):
        """Highlight the winning combination on the board."""
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == winner:
                self.buttons[i][0].config(bg="yellow")
                self.buttons[i][1].config(bg="yellow")
                self.buttons[i][2].config(bg="yellow")
                return
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == winner:
                self.buttons[0][i].config(bg="yellow")
                self.buttons[1][i].config(bg="yellow")
                self.buttons[2][i].config(bg="yellow")
                return
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == winner:
            self.buttons[0][0].config(bg="yellow")
            self.buttons[1][1].config(bg="yellow")
            self.buttons[2][2].config(bg="yellow")
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == winner:
            self.buttons[0][2].config(bg="yellow")
            self.buttons[1][1].config(bg="yellow")
            self.buttons[2][0].config(bg="yellow")
            return

def main():
    # Initialize the Tkinter root window
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
