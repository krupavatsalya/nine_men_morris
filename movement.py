#movement.py
def is_valid_move(board,player):
    print("Enter row and column for player: "+str(1 if player=='X' else 2))
    row,column=map(int,input().split())
    if board[row][column]=='0':
        board[row][column]=player
    else:
        print("Invalid Move")
        return is_valid_move(board,player)
    return board


def remove_mill(board,row,column,player):
    if(board[row][column]==player):
        board[row][column]='0'
    else:
        print("Invalid Move")
    return board