import tkinter as tk
import math


board = [" " for _ in range(9)]
buttons = []

player_score = 0
ai_score = 0

BG = "#0f172a"
BTN = "#1e293b"
HOVER = "#334155"

X_COLOR = "#22c55e"
O_COLOR = "#f43f5e"



# Check winner
def winner(b,p):
    win = [[0,1,2],[3,4,5],[6,7,8],
           [0,3,6],[1,4,7],[2,5,8],
           [0,4,8],[2,4,6]]
    for w in win:
        if b[w[0]]==b[w[1]]==b[w[2]]==p:
            animate_win(w)
            return True
    return False


def draw():
    return " " not in board


# Minimax AI
def minimax(b,depth,maximizing):

    if winner(b,"O"):
        return 1
    if winner(b,"X"):
        return -1
    if " " not in b:
        return 0

    if maximizing:
        best=-math.inf
        for i in range(9):
            if b[i]==" ":
                b[i]="O"
                score=minimax(b,depth+1,False)
                b[i]=" "
                best=max(score,best)
        return best
    else:
        best=math.inf
        for i in range(9):
            if b[i]==" ":
                b[i]="X"
                score=minimax(b,depth+1,True)
                b[i]=" "
                best=min(score,best)
        return best


# AI move
def ai_move():

    best=-math.inf
    move=None

    for i in range(9):
        if board[i]==" ":
            board[i]="O"
            score=minimax(board,0,False)
            board[i]=" "

            if score>best:
                best=score
                move=i

    board[move]="O"
    buttons[move]["text"]="O"
    buttons[move]["fg"]=O_COLOR
    

    check()


# Player move
def player(i):

    if board[i]==" ":
        board[i]="X"
        buttons[i]["text"]="X"
        buttons[i]["fg"]=X_COLOR
        

        if not check():
            window.after(300,ai_move)


# Check game
def check():

    global player_score,ai_score

    if winner(board,"X"):
        player_score+=1
        update_score()
        status["text"]="🎉 You Win!"
        disable()
        return True

    if winner(board,"O"):
        ai_score+=1
        update_score()
        status["text"]="🤖 AI Wins!"
        disable()
        return True

    if draw():
        status["text"]="Draw!"
        disable()
        return True

    return False


# Animate winning line
def animate_win(combo):

    for i in combo:
        buttons[i].config(bg="#22d3ee")


# Disable board
def disable():
    for b in buttons:
        b["state"]="disabled"


# Hover effect
def hover(e):
    e.widget["bg"]=HOVER

def leave(e):
    e.widget["bg"]=BTN


# Reset game
def reset():

    global board
    board=[" " for _ in range(9)]

    for b in buttons:
        b["text"]=""
        b["state"]="normal"
        b["bg"]=BTN

    status["text"]="Your Turn"


# Score update
def update_score():
    score_label["text"]=f"Player: {player_score}   AI: {ai_score}"


# Window
window=tk.Tk()
window.title("Neon Tic Tac Toe AI")
window.geometry("420x520")
window.configure(bg=BG)

title=tk.Label(window,text="⚡ Tic Tac Toe AI",
               font=("Arial",26,"bold"),
               fg="#38bdf8",
               bg=BG)
title.pack(pady=10)

score_label=tk.Label(window,
                     text="Player: 0   AI: 0",
                     font=("Arial",14),
                     bg=BG,
                     fg="white")
score_label.pack()

frame=tk.Frame(window,bg=BG)
frame.pack(pady=20)

# Grid
for i in range(9):

    btn=tk.Button(frame,
                  text="",
                  width=6,
                  height=3,
                  font=("Arial",28,"bold"),
                  bg=BTN,
                  fg="white",
                  relief="flat",
                  command=lambda i=i: player(i))

    btn.grid(row=i//3,column=i%3,padx=6,pady=6)

    btn.bind("<Enter>",hover)
    btn.bind("<Leave>",leave)

    buttons.append(btn)

status=tk.Label(window,
                text="Your Turn",
                font=("Arial",14),
                bg=BG,
                fg="white")
status.pack(pady=10)

restart=tk.Button(window,
                  text="Restart Game",
                  font=("Arial",12,"bold"),
                  bg="#22c55e",
                  relief="flat",
                  command=reset)

restart.pack(pady=10)

window.mainloop()