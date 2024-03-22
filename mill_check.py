def is_mill(board,piece, y, x):
    # Define the possible mill configurations as sets of coordinates
    mill_configurations = [
        {(0,0),(0,6),(0,12)},
        {(2,2),(2,6),(2,10)},
        {(4,4),(4,6),(4,8)},
        {(8,4),(8,6),(8,8)},
        {(10,2),(10,6),(10,10)},
        {(12,0),(12,6),(12,12)},
        {(6,0),(6,2),(6,4)},
        {(6,8),(6,10),(6,12)},
        {(0,0),(6,0),(12,0)},
        {(2,2),(6,2),(10,2)},
        {(4,4),(6,4),(8,4)},
        {(4,8),(6,8),(8,8)},
        {(2,10),(6,10),(10,10)},
        {(0,12),(6,12),(12,12)},
        {(0,6),(2,6),(4,6)},
        {(8,6),(10,6),(12,6)},
    ]
    # Check each mill configuration
    mills=[]
    # Check each mill configuration
    for config in mill_configurations:
        if (y,x) in config:
            mills.append(config)
    
    for config in mills:
        possible_mills=[board[i][j] for i,j in config]
        if possible_mills.count(piece)==3:
            return True

    return False
