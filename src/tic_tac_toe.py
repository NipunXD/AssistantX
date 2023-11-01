import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(root, text='', width=10, height=3,
                                                  command=lambda r=row, c=col: self.make_move(r, c))
                self.buttons[row][col].grid(row=row, column=col)

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state='disabled')
            if self.check_winner(row, col):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_board()
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

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

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
