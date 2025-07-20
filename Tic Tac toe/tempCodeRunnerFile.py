import tkinter as tk
from tkinter import messagebox
import time
import random

root = tk.Tk()
root.title("Tic-Tac-Toe AI (Unbeatable)")
root.configure(bg="#eaeaea")

current_player = "X"
ai_player = "O"
user_player = "X"

buttons = [[None for _ in range(3)] for _ in range(3)]
board = [["" for _ in range(3)] for _ in range(3)]

# Match stats
matches = wins = losses = draws = 0
stats_label = None

def update_stats(result):
    global matches, wins, losses, draws
    matches += 1
    if result == "win":
        wins += 1
    elif result == "loss":
        losses += 1
    elif result == "draw":
        draws += 1
    stats_label.config(text=f"Matches: {matches} | Wins: {wins} | Losses: {losses} | Draws: {draws}")

def check_winner(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != "":
            return b[i][0]
        if b[0][i] == b[1][i] == b[2][i] != "":
            return b[0][i]
    if b[0][0] == b[1][1] == b[2][2] != "":
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] != "":
        return b[0][2]
    return None

def is_draw(b):
    return all(b[i][j] != "" for i in range(3) for j in range(3))

def disable_buttons():
    for row in buttons:
        for btn in row:
            btn.config(state="disabled")

def ai_move():
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = ai_player
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        time.sleep(0.5)  # Delay to make AI look like it's thinking
        i, j = move
        board[i][j] = ai_player
        buttons[i][j].config(text=ai_player, state="disabled", disabledforeground="black", bg="#d3d3d3")
        winner = check_winner(board)
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            update_stats("loss" if winner == ai_player else "win")
            disable_buttons()
        elif is_draw(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            update_stats("draw")
            disable_buttons()

def minimax(b, depth, is_maximizing):
    result = check_winner(b)
    if result == ai_player:
        return 1
    elif result == user_player:
        return -1
    elif is_draw(b):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] == "":
                    b[i][j] = ai_player
                    score = minimax(b, depth + 1, False)
                    b[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] == "":
                    b[i][j] = user_player
                    score = minimax(b, depth + 1, True)
                    b[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

def on_click(i, j):
    if board[i][j] == "" and current_player == user_player:
        board[i][j] = user_player
        buttons[i][j].config(text=user_player, state="disabled", disabledforeground="black", bg="#d3d3d3")
        winner = check_winner(board)
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            update_stats("win")
            disable_buttons()
        elif is_draw(board):
            messagebox.showinfo("Game Over", "It's a draw!")
            update_stats("draw")
            disable_buttons()
        else:
            root.after(200, ai_move)

def restart():
    global board
    board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", state="normal", bg="#f8f8f8")
    choose_player()

def choose_player():
    global user_player, ai_player
    choice = messagebox.askquestion("Choose Player", "Do you want to go first?")
    if choice == "yes":
        user_player = "X"
        ai_player = "O"
    else:
        user_player = "O"
        ai_player = "X"
        root.after(300, ai_move)

# Create Buttons
for i in range(3):
    for j in range(3):
        btn = tk.Button(root, text=" ", width=6, height=3,
                        bg="#f8f8f8", fg="black", font=('Segoe UI', 20, 'bold'),
                        relief="solid", bd=1,
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j, padx=6, pady=6)
        buttons[i][j] = btn

# Restart Button
restart_btn = tk.Button(root, text="Restart", command=restart, font=('Segoe UI', 12, 'bold'),
                        bg="#c0c0c0", width=20)
restart_btn.grid(row=3, column=0, columnspan=3, pady=(10, 5))

# Stats label
stats_label = tk.Label(root, text="Matches: 0 | Wins: 0 | Losses: 0 | Draws: 0",
                       bg="#eaeaea", font=('Segoe UI', 12))
stats_label.grid(row=4, column=0, columnspan=3, pady=(0, 10))

choose_player()
root.mainloop()
