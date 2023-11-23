import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        # Use a more stylish font
        self.button_font = ("Helvetica", 14, "bold")

        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                # Use a larger button size
                self.buttons[row][col] = tk.Button(root, text='', width=10, height=3,
                                                  font=self.button_font, command=lambda r=row, c=col: self.make_move(r, c))
                self.buttons[row][col].grid(row=row, column=col, padx=5, pady=5)  # Add padding for better spacing

        # Add a label for displaying the current player
        self.player_label = tk.Label(root, text=f"Current Player: {self.current_player}", font=self.button_font)
        self.player_label.grid(row=3, column=0, columnspan=3)

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state='disabled', disabledforeground='black')

            if self.check_winner(row, col):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_board()
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.player_label.config(text=f"Current Player: {self.current_player}")

    def check_winner(self, row, col):
        player = self.current_player
        return (all(self.board[row][c] == player for c in range(3)) or
                all(self.board[r][col] == player for r in range(3)) or
                all(self.board[i][i] == player for i in range(3)) or
                all(self.board[i][2 - i] == player for i in range(3)))

    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.board[row][col] = ' '
                self.buttons[row][col].config(text='', state='active')
        self.current_player = 'X'
        self.player_label.config(text=f"Current Player: {self.current_player}")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
