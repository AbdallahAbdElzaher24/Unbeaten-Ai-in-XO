import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Tic Tac Toe")

player = "X"
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
turn_label = tk.Label(root, text="Player X's turn", font=('normal', 20))
turn_label.grid(row=0, column=0, columnspan=3)


def create_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(root, text="", font=('normal', 40), width=5, height=2,
                                      command=lambda i=i, j=j: on_click(i, j))
            buttons[i][j].grid(row=i + 1, column=j)


def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]


    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]

    return None


def is_draw():
    for row in board:
        if "" in row:
            return False
    return True


def on_click(i, j):
    global player
    if buttons[i][j]["text"] == "" and player == "X":
        buttons[i][j].config(text=player, fg="blue")
        board[i][j] = player

        winner = check_winner()
        if winner:
            messagebox.showinfo("Game Over", " AI wins!")
            disable_buttons()
            return
        elif is_draw():
            messagebox.showinfo("Game Over", "It's a Draw!")
            disable_buttons()
            return

        player = "O"
        turn_label.config(text="AI is thinking...")
        root.update_idletasks()
        root.after(600, ai_move)


def minimax(board, depth, is_maximizing):
    winner = check_winner()
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score


def ai_move():
    global player
    best_score = -float("inf")
    move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)

    if move:
        i, j = move
        board[i][j] = "O"
        buttons[i][j].config(text="O", fg="red")

        winner = check_winner()
        if winner:
            messagebox.showinfo("Game Over", " AI  wins!")
            disable_buttons()
            return
        elif is_draw():
            messagebox.showinfo("Game Over", "It's a Draw!")
            disable_buttons()
            return

        player = "X"
        turn_label.config(text="Player X's turn")


def disable_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state="disabled")


def reset_board():
    global board, player
    player = "X"
    turn_label.config(text="Player X's turn")
    board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j]["text"] = ""
            buttons[i][j].config(state="normal")


reset_button = tk.Button(root, text="Reset Game", font=('normal', 20), command=reset_board)
reset_button.grid(row=4, column=0, columnspan=3)

create_buttons()
root.mainloop()