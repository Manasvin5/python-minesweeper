import tkinter as tk
import random

class Minesweeper:
    def __init__(self, master, rows=10, columns=10, mines=10):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.board = []
        self.buttons = []

        self.create_widgets()
        self.place_mines()
        self.calculate_numbers()

    def create_widgets(self):
        for row in range(self.rows):
            row_buttons = []
            for col in range(self.columns):
                button = tk.Button(self.master, width=2, height=1, command=lambda r=row, c=col: self.reveal_cell(r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.toggle_flag(event, r, c))
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def place_mines(self):
        self.board = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.columns - 1)
            if self.board[row][col] != 'M':
                self.board[row][col] = 'M'
                mines_placed += 1

    def calculate_numbers(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] != 'M':
                    self.board[row][col] = self.count_adjacent_mines(row, col)

    def count_adjacent_mines(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.columns and self.board[r][c] == 'M':
                count += 1
        return count

    def reveal_cell(self, row, col):
        if self.board[row][col] == 'M':
            self.buttons[row][col].config(text='M', bg='red')
            self.game_over(False)
        else:
            self.buttons[row][col].config(text=self.board[row][col], state=tk.DISABLED)
            if self.board[row][col] == 0:
                self.reveal_adjacent_cells(row, col)

    def reveal_adjacent_cells(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.columns and self.buttons[r][c]['state'] == tk.NORMAL:
                self.reveal_cell(r, c)

    def toggle_flag(self, event, row, col):
        button = self.buttons[row][col]
        if button['text'] == '':
            button.config(text='F', fg='red')
        elif button['text'] == 'F':
            button.config(text='')

    def game_over(self, won):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] == 'M':
                    self.buttons[row][col].config(text='M')
        if won:
            print("You won!")
        else:
            print("Game over!")

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
