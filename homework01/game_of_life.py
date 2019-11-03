# Homework 01 - Game of life
# 
# Your task is to implement part of the cell automata called
# Game of life. The automata is a 2D simulation where each cell
# on the grid is either dead or alive.
# 
# State of each cell is updated in every iteration based state of neighbouring cells.
# Cell neighbours are cells that are horizontally, vertically, or diagonally adjacent.
#
# Rules for update are as follows:
# 
# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# 2. Any live cell with two or three live neighbours lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
#
# 
# Our implementation will use coordinate system will use grid coordinates starting from (0, 0) - upper left corner.
# The first coordinate is row and second is column.
# 
# Do not use wrap around (toroid) when reaching edge of the board.
# 
# For more details about Game of Life, see Wikipedia - https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

# Updates the state of cell automata.
def update(alive, size, iter_n):

    # Sets of previous and next generations.
    prev_gen = alive.copy()
    next_gen = set()

    # Iterates through states.
    for _ in range(iter_n):
    
        next_gen.clear()
        
        # Browses the grid.
        for x in range(size[0]):
            for y in range(size[1]):
            
                neighbours = 0
                
                # Explores neighbours.
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                    
                        # Edges and avoiding the current cell.
                        if (i < 0 or i >= size[0] or
                            j < 0 or j >= size[1] or
                            (i == x and j == y)):
                            continue
                        
                        # The neighbour is living.
                        if (i, j) in prev_gen:
                            neighbours += 1
                        
                # The case of living cell.
                if (x, y) in prev_gen:
                    
                    # The living cell dies.
                    if neighbours < 2 or neighbours > 3:
                        pass
                    
                    # The living cell survives.
                    if neighbours == 2 or neighbours == 3:
                        next_gen.add((x, y));
                
                # The case of dead cell.
                if (x, y) not in prev_gen:
                
                    # The dead cell comes back to life.
                    if neighbours == 3:
                        next_gen.add((x, y))
        
        # Generations are shifted.
        prev_gen = next_gen.copy()
    
    return next_gen

# Draws the state of cell automata.
def draw(alive, size):

    # The upper row
    str_out = "+"
    for _ in range(size[1]):
        str_out += "-"
    str_out += "+\n"
    
    # The grid
    for rows in range(size[0]):
        str_out += "|"
        
        for cols in range(size[1]):
            if (rows, cols) in alive:
                str_out += "X"
            else:
                str_out += " "
                
        str_out += "|\n"

    # The lower row
    str_out += "+"
    for _ in range(size[1]):
        str_out += "-"
    str_out += "+"

    return str_out
