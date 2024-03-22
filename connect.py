import tkinter as tk

class ConnectFour:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect Four")
        self.current_player = 'X'
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.buttons = [[None for _ in range(7)] for _ in range(6)]

        for i in range(6):
            for j in range(7):
                self.buttons[i][j] = tk.Button(self.root, text='', font=('normal', 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_button_click(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            self.check_and_remove_opponent(row, col)
            self.switch_player()

    def check_and_remove_opponent(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Check horizontally, vertically, and diagonally
        for dr, dc in directions:
            count = 1
            count += self.count_in_direction(row, col, dr, dc)
            count += self.count_in_direction(row, col, -dr, -dc)
            if count >= 3:
                self.remove_opponent(row, col, dr, dc)

    def count_in_direction(self, row, col, dr, dc):
        count = 0
        while 0 <= row + dr < 6 and 0 <= col + dc < 7 and self.board[row + dr][col + dc] == self.current_player:
            count += 1
            row += dr
            col += dc
        return count

    def remove_opponent(self, row, col, dr, dc):
        for _ in range(3):
            row += dr
            col += dc
            self.board[row][col] = ' '
            self.buttons[row][col].config(text='')

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = ConnectFour()
    game.run()
