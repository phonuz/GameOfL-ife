import numpy
import random
import globals

CELLS_WIDTH = 80
CELLS_HEIGHT = 80
CELLS_HALF_WIDTH = CELLS_WIDTH // 2
CELLS_HALF_HEIGHT = CELLS_HEIGHT // 2

CELLS_LEFT_X = globals.SCREEN_CENTER_X - CELLS_HALF_WIDTH
CELLS_RIGHT_X = globals.SCREEN_CENTER_X + CELLS_HALF_WIDTH

CELLS_TOP_Y = globals.SCREEN_CENTER_Y - CELLS_HALF_HEIGHT
CELLS_BOTTOM_Y = globals.SCREEN_CENTER_Y + CELLS_HALF_HEIGHT

CELL_SIZE = 10

CELL_MARGIN = globals.SCREEN_CENTER_X - (CELLS_HALF_WIDTH * CELL_SIZE)

ODDS_OF_PERSON = 65

############################################################################
# Game of Life
#
# Any live cell with two or three live neighbours survives.
# Any dead cell with three live neighbours becomes a live cell.
# All other live cells die in the next generation. Similarly, all other dead cells stay dead.
#
class GameOfLife:
    # Initialization function
    #   1. Create the class variable cellIndex
    #   2. Create a numpy 3 dimensional array called "cells" with:
    #       -> x position in the cells grid
    #       -> y position in the cells grid
    #       -> an index because we want two versions of the grid (now and next)
    #
    def __init__(self):
        self.cellIndex = 0
        self.cells = numpy.empty((CELLS_WIDTH, CELLS_HEIGHT, 2), dtype=object)

    # Seed cells function
    #   1. Set the cell index to 0
    #   2. Fill all cells with the EMPTY COLOR value
    #   3. Generate random People in the grid
    #
    def seedCells(self):
        self.cellIndex = 0
        self.cells.fill(globals.EMPTY_COLOR)

        for x in range(0, CELLS_WIDTH):
            for y in range(0, CELLS_HEIGHT):
                if random.randint(1,100) > ODDS_OF_PERSON:
                    self.cells[x,y, self.cellIndex] = globals.PEOPLE_COLORS[random.randrange(0, len(globals.PEOPLE_COLORS))]

    # Update cells function
    #   1. Set a variable "nextCellIndex" to 0 if cellIndex was 1 and 1 if cellIndex was 0 (to flip between the two)
    #   2. Clean all the cells in the next grid page (set all to EMPTY COLOR)
    #   3. Walk through each cell of the current grid and:
    #       a. Count neighbors including how many are alive
    #       b. Any live cell with two or three live neighbours survives.
    #       c. Any dead cell with three live neighbours becomes a live cell.
    #       d. All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    #       e. Set the current cell page index to the next index
    #
    def updateCells(self):
        nextCellIndex = int(not(self.cellIndex))
        self.cleanCells(nextCellIndex)

        # Iterate through all the Cells in the current cell page index
        for x in range(0, CELLS_WIDTH):
            for y in range(0, CELLS_HEIGHT):
                
                numNeighbours = 0

                # Iterate through the up to 8 surrounding cells to detect and count neighbors
                for i in range(-1,2):
                    for j in range(-1,2):

                        # Ignore when i == 0 and j == 0 because that is the current cell itself
                        if not(i == 0 and j == 0):
                            col = x + i
                            row = y + j

                            # Only check for a neighbor if the surrounding cell is in bounds
                            if col >= 0 and col < CELLS_WIDTH and row >= 0 and row < CELLS_HEIGHT:

                                # Anything other than EMPTY counts as a neighbor
                                if self.cells[col, row, self.cellIndex] != globals.EMPTY_COLOR:
                                    numNeighbours += 1            

                currentColor = self.cells[x,y, self.cellIndex] 
                
                if currentColor == globals.EMPTY_COLOR:
                    if numNeighbours == 3:
                        self.cells[x,y, nextCellIndex] = globals.PEOPLE_COLORS[random.randrange(0, len(globals.PEOPLE_COLORS))]
                    else:
                        self.cells[x,y, nextCellIndex] = globals.EMPTY_COLOR
                else:
                    if  numNeighbours < 2 or numNeighbours > 3:
                        self.cells[x,y, nextCellIndex] = globals.EMPTY_COLOR
                    else:
                        self.cells[x,y, nextCellIndex] = self.cells[x,y, self.cellIndex]
                    
        self.cellIndex = nextCellIndex        

    # Clean cells function
    #   1. Iterate through all cells in the given cell page index
    #   2. Set their color to EMPTY
    #
    def cleanCells(self, index):
        for x in range(0, CELLS_WIDTH):
            for y in range(0, CELLS_HEIGHT):
                self.cells[x,y, index] = globals.EMPTY_COLOR
    
    # "Get the Screen X coordinate for a given Cell grid X value" function
    #   Return the value of multiplying the grid X times the Cell size and then adding the cell margin offset
    #
    def screenX(self, x):
        return (x * CELL_SIZE) + CELL_MARGIN

    # "Get the Screen Y coordinate for a given Cell grid Y value" function
    #   Return the value of multiplying the grid Y times the Cell size and then adding the cell margin offset
    #
    def screenY(self, y):
        return (y * CELL_SIZE) + CELL_MARGIN
    
    # Draw cells function
    #   1. Receive a parameter that is an external "draw" function that will know how to actually draw via pygame
    #   2. Iterate through the Cells in the current cell grid page
    #       a. If the cell is not EMPTY then draw that cell using the color of the cell
    #
    def drawCells(self, draw):

        for x in range(0, CELLS_WIDTH):
            for y in range(0, CELLS_HEIGHT):
                color = self.cells[x,y, self.cellIndex]
                if color != globals.EMPTY_COLOR:
                    draw( color, self.screenX(x), self.screenY(y), CELL_SIZE )