import tkinter as tk
from tkinter import messagebox
import json
import random

USER_DATA_FILE = "users.json"

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

class MinesweeperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper Login")
        self.root.geometry("300x200")
        self.root.configure(bg="#1c1c1c")

        
        self.users = load_user_data()

        
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(root, text="Username:", bg="#1c1c1c", fg="#ffffff").pack(pady=10)
        self.username_entry = tk.Entry(root, textvariable=self.username_var, bg="#333333", fg="#ffffff")
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:", bg="#1c1c1c", fg="#ffffff").pack(pady=10)
        self.password_entry = tk.Entry(root, textvariable=self.password_var, show="*", bg="#333333", fg="#ffffff")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Login", command=self.login, bg="#444444", fg="#ffffff").pack(pady=5)
        tk.Button(root, text="Register", command=self.register, bg="#444444", fg="#ffffff").pack(pady=5)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if username in self.users and self.users[username] == password:
            messagebox.showinfo("Login", "Login successful!")
            self.root.destroy()
            self.launch_minesweeper()
        else:
            messagebox.showerror("Login", "Invalid username or password")

    def register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if username in self.users:
            messagebox.showerror("Register", "Username already exists!")
        else:
            self.users[username] = password
            save_user_data(self.users)
            messagebox.showinfo("Register", "Registration successful!")

    def launch_minesweeper(self):
        game_window = tk.Tk()
        Minesweeper(game_window)
        game_window.mainloop()

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.configure(bg="#1c1c1c")
        self.grid_size = 10
        self.mine_count = 15
        self.buttons = []
        self.mines = set()
        self.flags = set()

        self.create_widgets()
        self.place_mines()
        self.update_button_counts()

    def create_widgets(self):
        for r in range(self.grid_size):
            row = []
            for c in range(self.grid_size):
                btn = tk.Button(self.root, text="", width=3, height=1, bg="#333333", fg="#ffffff",
                                command=lambda r=r, c=c: self.reveal_cell(r, c))
                btn.bind("<Button-3>", lambda event, r=r, c=c: self.flag_cell(r, c))
                btn.grid(row=r, column=c, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)

        self.status_label = tk.Label(self.root, text="", bg="#1c1c1c", fg="#ffffff")
        self.status_label.grid(row=self.grid_size, column=0, columnspan=self.grid_size, pady=10)

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game, bg="#444444", fg="#ffffff")
        self.restart_button.grid(row=self.grid_size + 1, column=0, columnspan=self.grid_size, pady=10)

    def place_mines(self):
        while len(self.mines) < self.mine_count:
            r = random.randint(0, self.grid_size - 1)
            c = random.randint(0, self.grid_size - 1)
            self.mines.add((r, c))

    def update_button_counts(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if (r, c) not in self.mines:
                    count = self.count_adjacent_mines(r, c)
                    self.buttons[r][c].mine_count = count

    def count_adjacent_mines(self, r, c):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        count = 0
        for dr, dc in directions:
            if 0 <= r + dr < self.grid_size and 0 <= c + dc < self.grid_size:
                if (r + dr, c + dc) in self.mines:
                    count += 1
        return count

    def reveal_cell(self, r, c):
        if (r, c) in self.mines:
            self.game_over(False)
            return

        btn = self.buttons[r][c]
        if btn["state"] == "disabled":
            return

        count = self.buttons[r][c].mine_count
        btn.config(text=str(count) if count > 0 else "", state="disabled", bg="#555555")

        if count == 0:
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1),         (0, 1),
                           (1, -1), (1, 0), (1, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                    self.reveal_cell(nr, nc)

        if self.check_win():
            self.game_over(True)

    def flag_cell(self, r, c):
        btn = self.buttons[r][c]
        if btn["state"] == "disabled":
            return

        if (r, c) in self.flags:
            btn.config(text="", bg="#333333")
            self.flags.remove((r, c))
        else:
            btn.config(text="F", bg="#888888")
            self.flags.add((r, c))

    def check_win(self):
        revealed_cells = sum(btn["state"] == "disabled" for row in self.buttons for btn in row)
        return revealed_cells == self.grid_size ** 2 - self.mine_count

    def game_over(self, won):
        if won:
            self.status_label.config(text="You won!")
        else:
            self.status_label.config(text="Game Over!")
            for r, c in self.mines:
                self.buttons[r][c].config(text="M", bg="#ff6666")

        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def restart_game(self):
        self.root.destroy()
        self.__init__(tk.Tk())

if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperApp(root)
    root.mainloop()
