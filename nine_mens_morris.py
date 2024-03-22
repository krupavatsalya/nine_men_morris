import tkinter as tk
from construction_board import construct
from mill_check import is_mill
from tkinter import messagebox
import random 
# import os
# from datetime import datetime


row_length = 13
board = [[' ' for _ in range(row_length)] for _ in range(row_length)]
board = construct(board)
players = ['X', 'O']
current_player_index = 0
remaining_pieces = {'X': 9, 'O': 9}
removed_pieces = {'X': 0, 'O': 0}
placed_positions={'X':[],'O':[]}
possible_removal_pieces=[]
movement_order=[]
total_pieces=[(0,0),(0,6),(0,12),(2,2),(2,6),(2,10),(4,4),(4,6),(4,8),(6,0),(6,2),(6,4),(6,8),(6,10),(6,12),(8,4),(8,6),(8,8),(10,2),(10,6),(10,10),(12,0),(12,6),(12,12)]
nearest_neighbors={
    (0, 0): [(0, 6), (6, 0)], 
    (0, 6): [(0, 12), (2, 6), (0, 0)], 
    (0, 12): [(6, 12), (0, 6)], 
    (2, 2): [(2, 6), (6, 2)], 
    (2, 6): [(2, 10), (4, 6), (2, 2), (0, 6)], 
    (2, 10): [(6, 10), (2, 6)], 
    (4, 4): [(4, 6), (6, 4)], 
    (4, 6): [(4, 8), (4, 4), (2, 6)], 
    (4, 8): [(6, 8), (4, 6)], 
    (6, 0): [(6, 2), (12, 0), (0, 0)], 
    (6, 2): [(6, 4), (10, 2), (6, 0), (2, 2)], 
    (6, 4): [(6, 8), (6, 2), (4, 4)], 
    (6, 8): [(6, 10), (8, 8), (4, 8)], 
    (6, 10): [(6, 12), (10, 10), (6, 8), (2, 10)], 
    (6, 12): [(12, 12), (6, 10), (0, 12)], 
    (8, 4): [(8, 6), (6, 4)], 
    (8, 6): [(8, 8), (10, 6), (8, 4)], 
    (8, 8): [(8, 6), (6, 8)], 
    (10, 2): [(10, 6), (6, 2)], 
    (10, 6): [(10, 10), (12, 6), (10, 2), (8, 6)], 
    (10, 10): [(10, 6), (6, 10)],
    (12, 0): [(12, 6), (6, 0)], 
    (12, 6): [(12, 12), (12, 0), (10, 6)], 
    (12, 12): [(12, 6), (6, 12)]
    }
possible_movement=[]
present_y=0
present_x=0
game_started = False
opponent_piece='O'
button="<Button -1>"

root = tk.Tk()
root.title("Nine Men's Morris")

canvas = tk.Canvas(root, width=400, height=500, bg='white')
canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
symbol_text = None
remaining_pieces_text = None
computer_piece='O'
computer_game=False

canvas.focus_set()

# Display methods
def display_current_player_symbol():
    global symbol_text
    if symbol_text:
        canvas.delete(symbol_text)  # Remove the previous symbol

    current_player = players[current_player_index]
    symbol_x = 200  # X-coordinate for the symbol
    symbol_y = 420  # Y-coordinate for the symbol (above the board)

    if current_player == 'X':
        symbol_text = canvas.create_text(symbol_x, symbol_y, text='Current Player: Player 1, Symbol: X', font=("Arial", 12))
    else:
        symbol_text = canvas.create_text(symbol_x, symbol_y, text='Current Player: Player 2, Symbol: O', font=("Arial", 12))

def display_current_remaining_pieces():
    global remaining_pieces_text
    if remaining_pieces_text:
        canvas.delete(remaining_pieces_text)  # Remove the previous text
    current_player = players[current_player_index]
    remaining_pieces_string = f"Remaining Pieces of {current_player}: {remaining_pieces[current_player]}"
    removed_pieces_string=f"Removed Pieces of {current_player}:{removed_pieces[current_player]}"
    symbol_x = 200  # X-coordinate for the text
    symbol_y = 450  # Y-coordinate for the text (above the board)
    remaining_pieces_text = canvas.create_text(symbol_x, symbol_y, text=remaining_pieces_string+"\n"+removed_pieces_string, font=("Arial", 12))

def display_game_name():
    canvas.create_text(200, 50, text="Nine Men's Morris", font=("Arial", 16, "bold"))


# game board
def draw_board():
    canvas.delete("all")  # Display the game name
    for i in range(row_length):
        for j in range(row_length):
            x = j * 30
            y = i * 30
            if board[i][j] != ' ':
                canvas.create_text(x + 15, y + 15, text=board[i][j], font=("Consolas", 12))

#Player to Player

def removing_valid_piece(event):
    global opponent_piece,possible_removal_pieces
    x = event.x // 30
    y = event.y // 30
    remove_tuple=(y,x)
    check_mills = {} 
    for position in placed_positions[opponent_piece]:
        # Convert the position list to a tuple
        position_tuple = tuple(position)
        check_mills[position_tuple] = is_mill(board, opponent_piece, position[0], position[1])
    # Use list comprehension to filter out True values
    if len(check_mills)!=list(check_mills.values()).count(True):
        check_mills = {key: val for key, val in check_mills.items() if val is not True}
    possible_removal_pieces = list(check_mills.keys())
    if remove_tuple in possible_removal_pieces:
        board[y][x] = '0'
        placed_positions[opponent_piece].remove((y,x))
        removed_pieces[opponent_piece]+=1
        draw_board()
        if removed_pieces[opponent_piece]==7:
            announce_winner()
            return
        canvas.bind(button, place_piece) 
        display_current_player_symbol()
        display_current_remaining_pieces()
    
def remove_piece():
    global opponent_piece
    opponent_piece = players[1 - current_player_index]
    canvas.bind(button, removing_valid_piece)


def movement(event):
    global is_possible,current_player_index,opponent_piece,possible_movement
    current_player=players[1-current_player_index] if computer_game==False else 'X'
    x = event.x // 30
    y = event.y // 30
    if removed_pieces[current_player]==6:
        board[present_y][present_x]='0'
        placed_positions[current_player].remove((present_y,present_x))
        if board[y][x]=='0':
            board[y][x]=current_player
            placed_positions[current_player].append((y,x))
            draw_board()
    else:
        if (y,x) in possible_movement:
            board[present_y][present_x]='0'
            placed_positions[current_player].remove((present_y,present_x))
            board[y][x]=current_player
            placed_positions[current_player].append((y,x))
    if is_mill(board,current_player,y,x):
        remove_piece()
        draw_board()
        opponent_piece=players[current_player_index]
    else:
        if computer_game:
            canvas.bind(button,place_piece_computer)
        else:
            canvas.bind(button, place_piece) 
    draw_board()
    display_current_player_symbol()
    display_current_remaining_pieces()
            
def format_data(board):
    formatted_data=""
    for _ in range(len(board)):
        formatted_data+="".join(board[_])
    return formatted_data

def place_piece(event):
    global current_player_index,present_x,present_y,possible_movement,file_name           
    current_player = players[current_player_index]
    if remaining_pieces[current_player] > 0:
        x = event.x // 30
        y = event.y // 30
        if board[y][x] == '0':
            board[y][x] = current_player
            placed_positions[current_player].append((y,x))
            remaining_pieces[current_player] -= 1
            movement_order.append((y,x))
            if is_mill(board,current_player,y,x):
                remove_piece()
            draw_board()
            current_player_index = 1 - current_player_index
            display_current_player_symbol()
            display_current_remaining_pieces()
    else:
        x = event.x // 30
        y = event.y // 30
        possible_movement=[]
        present_x=x
        present_y=y
        neighbors=nearest_neighbors[(y,x)]
        if board[y][x]==current_player and removed_pieces[current_player]<6:
                for element in neighbors:
                    if all(element not in value for value in placed_positions.values()):
                        possible_movement.append(element)
        if len(possible_movement)!=0 or removed_pieces[current_player]==6:
            canvas.bind(button,movement)
            display_current_player_symbol()
            display_current_remaining_pieces()
            current_player_index = 1 - current_player_index

# Player Vs Computer

def remove_valid_computer(event):
    global opponent_piece,possible_removal_pieces
    x = event.x // 30
    y = event.y // 30
    remove_tuple=(y,x)
    check_mills = {} 
    for position in placed_positions[opponent_piece]:
        # Convert the position list to a tuple
        position_tuple = tuple(position)
        check_mills[position_tuple] = is_mill(board, opponent_piece, position[0], position[1])
    # Use list comprehension to filter out True values
    if len(check_mills)!=list(check_mills.values()).count(True):
        check_mills = {key: val for key, val in check_mills.items() if val is not True}
    possible_removal_pieces = list(check_mills.keys())
    if remove_tuple in possible_removal_pieces:
        board[y][x] = '0'
        placed_positions[opponent_piece].remove((y,x))
        total_pieces.append((y,x))
        removed_pieces[opponent_piece]+=1
        draw_board()
        if removed_pieces[opponent_piece]==7:
            announce_winner()
            return
        computer_place()
        canvas.bind(button, place_piece_computer) 
        display_current_player_symbol()
        display_current_remaining_pieces()

def remove_piece_of_computer():
    global opponent_piece
    opponent_piece = 'O'
    canvas.bind(button, remove_valid_computer)

def remove_piece_by_computer():
    global possible_removal_pieces
    check_mills = {} 
    for position in placed_positions['X']:
        position_tuple = tuple(position)
        check_mills[position_tuple] = is_mill(board, 'X', position[0], position[1])
    if len(check_mills)!=list(check_mills.values()).count(True):
        check_mills = {key: val for key, val in check_mills.items() if val is not True}
    possible_removal_pieces = list(check_mills.keys())
    (y,x)=random.choice(possible_removal_pieces)
    board[y][x] = '0'
    placed_positions['X'].remove((y,x))
    total_pieces.append((y,x))
    removed_pieces['X']+=1
    draw_board()
    if removed_pieces['X']==7:
        announce_winner()
        return
    canvas.bind(button, place_piece_computer) 
    display_current_player_symbol()
    display_current_remaining_pieces()

def movement_against_computer(event, possible_movement):
    global is_possible, current_player_index, opponent_piece

    x = event.x // 30
    y = event.y // 30
    current_player = 'X'  # Assuming 'X' is the player symbol


    if removed_pieces[current_player] == 6:
        board[present_y][present_x] = '0'
        placed_positions[current_player].remove((present_y, present_x))
        if board[y][x] == '0':
            board[y][x] = current_player
            placed_positions[current_player].append((y, x))
            draw_board()
    else:
        if (y, x) in possible_movement:
            board[present_y][present_x] = '0'
            placed_positions[current_player].remove((present_y, present_x))
            board[y][x] = current_player
            placed_positions[current_player].append((y, x))

    if is_mill(board, current_player, y, x):
        remove_piece_of_computer()
        draw_board()
    else:
        # Assuming 'button' is a variable you have defined earlier
        canvas.bind(button, place_piece_computer)

    while True:
        possible_movement=[]
        y, x = random.choice(placed_positions['O'])
        neighbors = nearest_neighbors[(y, x)]

        if board[y][x] == 'O' and removed_pieces[current_player] < 6:
            for element in neighbors:
                if all(element not in value for value in placed_positions.values()):
                    possible_movement.append(element)
        if len(possible_movement)==0:
            continue
        new_y, new_x = random.choice(list(possible_movement))
        board[y][x] = '0'
        placed_positions['O'].remove((y, x))
        board[new_y][new_x] = 'O'
        placed_positions[current_player].append((y, x))
        possible_movement.remove((new_y, new_x))
        possible_movement.append((y, x))
        print(y,x,new_x,new_y)
        if is_mill(board, current_player, y, x):
            remove_piece_by_computer()
            draw_board()
        if len(possible_movement) != 0:
            break

    draw_board()
    display_current_player_symbol()
    display_current_remaining_pieces()
    canvas.update_idletasks()



def computer_place():
    # AI's move: Randomly select a position and place a piece
    if remaining_pieces['O']>0:
        computer_placement = random.choice(total_pieces)
        total_pieces.remove(computer_placement)
        board[computer_placement[0]][computer_placement[1]] = 'O'
        placed_positions['O'].append(computer_placement)
        remaining_pieces['O'] -= 1

        # Computer's move: Check for a mill and remove player's piece if necessary
        if is_mill(board, 'O', computer_placement[0], computer_placement[1]):
            remove_piece_by_computer()

        draw_board()
        display_current_player_symbol()
        display_current_remaining_pieces()
        canvas.update_idletasks()
    else:
        return

def place_piece_computer(event):
    global total_pieces,computer_piece,present_x,present_y
    if game_started:
        current_player='X'
        if remaining_pieces[current_player] > 0:
            x = event.x // 30
            y = event.y // 30
            if board[y][x] == '0':
                # Player's move
                board[y][x] = current_player
                placed_positions[current_player].append((y, x))
                remaining_pieces[current_player] -= 1
                movement_order.append((y, x))
                total_pieces.remove((y, x))
                draw_board()

                # Check if the player has formed a mill
                if is_mill(board, current_player, y, x):
                    # Player has a mill, initiate player's removal process
                    remove_piece_of_computer()
                else:
                    # Player doesn't have a mill, proceed with AI's move
                    computer_place()
        else:
            x = event.x // 30
            y = event.y // 30
            possible_movement=[]
            present_x=x
            present_y=y
            neighbors=nearest_neighbors[(y,x)]
            if board[y][x]==current_player and removed_pieces[current_player]<6:
                    for element in neighbors:
                        if all(element not in value for value in placed_positions.values()):
                            possible_movement.append(element)
            if len(possible_movement)!=0:
                canvas.bind("<Button-1>", lambda event: movement_against_computer(event, possible_movement))
                display_current_player_symbol()
                display_current_remaining_pieces()
            

# Game operations

def reset_game():
    global board, current_player_index, remaining_pieces, game_started, players,removed_pieces
    board = [[' ' for _ in range(row_length)] for _ in range(row_length)]
    players = ['X', 'O']
    current_player_index = 0
    remaining_pieces = {'X': 9, 'O': 9}
    removed_pieces={'X':0,'O':0}
    game_started = False

def start_game():
    global game_started, board
    canvas.bind(button, place_piece)
    game_started = True
    display_game_name()
    board = construct(board)
    draw_board()
    display_current_player_symbol()
    display_current_remaining_pieces()

def start_game_with_computer():
    global game_started, board,computer_game
    canvas.bind(button, place_piece_computer)
    game_started = True
    computer_game=True
    display_game_name()
    board = construct(board)
    draw_board()
    display_current_player_symbol()
    display_current_remaining_pieces()

def main_menu():
    global game_started,board
    reset_game()
    draw_board()
    display_game_name()

def announce_winner():
    if game_started:
        winner='X' if removed_pieces['O']==7 else 'O'
        winner = "Player 1" if winner == "X" else "Player 2"
        messagebox.showinfo("Winner", f"The winner is {winner}!")
        reset_game()
        draw_board()
        display_game_name()

def end_game():
    global current_player_index, game_started
    if game_started:
        announce_winner()
        reset_game()
        draw_board()
        display_game_name()

start_button = tk.Button(root, text="Player vs Player", command=start_game)
start_game_with_computer_button=tk.Button(root,text="Player vs Computer",command=start_game_with_computer)
main_menu_button = tk.Button(root, text="Main Menu", command=main_menu)
end_game_button = tk.Button(root, text="End Game", command=end_game)


start_button.grid(row=1, column=0, padx=10, pady=10)
start_game_with_computer_button.grid(row=1,column=1,padx=10,pady=10)
main_menu_button.grid(row=1, column=2, padx=10, pady=10)
end_game_button.grid(row=1, column=3, padx=10, pady=10)
display_game_name()
# Start the GUI main loop
root.mainloop()