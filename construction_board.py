#construction_board.py
def set_connections(board):
    row_length = len(board)
    vertex_point = [0, 2, 4]
    connectors = ['-', '|']
    for connector in range(2):
        for vertex in vertex_point:
            for row_index in range(vertex, row_length - vertex):
                for column_index in range(row_length):
                    if (column_index == vertex or column_index == row_length - vertex - 1) and board[row_index][column_index] != '0':
                        board[row_index * connector + column_index * (1 - connector)][column_index * connector + row_index * (1 - connector)] = connectors[connector]
        for column_index in range(row_length):
            if column_index in vertex_point[:-1] or column_index in [row_length - vertex - 1 for vertex in vertex_point[1:]]:
                board[6 * connector + (column_index + 1) * (1 - connector)][6 * (1 - connector) + (column_index + 1) * connector] = connectors[1 - connector]
    return board

def construct(board):
    length = len(board)
    for row_index in range(length):
        if row_index % 2 != 0:
            continue
        for column_index in range(row_index, length):
            if ((row_index + column_index == 12 or row_index == column_index) and row_index != 6) or ((row_index == 6 or column_index == 6) and (column_index % 2 == 0) and column_index != row_index):
                board[row_index][column_index] = '0'
                board[column_index][row_index] = '0'
    
    set_connections(board)
    return board