import numpy as np
import random
from time import sleep

class CellularAutomata:
    """This class is primarily used for calculating the values of any grid (dimensions
        determined by the number of columns and rows passed into the constructor). This class
        will not alter or update the colors based on these values."""
    
    numRows = 0 # These will be assigned to the dimensions of the sense matrix dimensions.
    numCols = 0 # These will be assigned to the dimensions of the sense matrix dimensions.
    current_state = None # Empty 2d Array that will represent the cells' current states.
    next_state = None # Empty 2d array that will represent the cells' next states.
    sense = None # Used to access sense hat matrix.
    alive = (0, 255, 0) # RGB values
    dead = (0, 0, 0) # RGB values
    isStillIterations = 0 # Used to calcualte if the cells are still.
    isStill = False # Used to determine if the cells are still.
    
    def __init__(self, numRows, numCols):
        print("CA Initialized!")
        self.numRows = numRows
        self.numCols = numCols
        self.current_state = np.zeros((self.numRows, self.numCols))
        self.next_state = np.zeros((self.numRows, self.numCols))
        
    def clear_cell_states(self):
        self.current_state = np.zeros((self.numRows, self.numCols))
        
    def randomize_cell_states(self):
        for y in range(self.numRows):
            for x in range(self.numCols):
                random_number = random.randrange(1, 100)
                if random_number < 50:
                    self.current_state[y, x] = 1
                else:
                    self.current_state[y, x] = 0
                    
    def get_current_cells(self):
        return self.current_state
    
    def get_next_cell(self):
        return self.next_state
                            
    def get_nearby_neighbors(self, rowPos, colPos):
        count = 0
        for y in range(-1, 2):
            for x in range(-1, 2):
                row = (rowPos + y + 8) % 8
                col = (colPos + x + 8) % 8
                
                if self.current_state[row, col] == 1:
                    count += 1
        
        if self.current_state[rowPos, colPos] == 1:
            count -= 1
        
        return count
    
    def check_stillness(self):
        self.isStill = False
        if np.array_equal(self.current_state, self.next_state):
            # If there is no change, then game is still
            self.isStill = True
            
    def is_still(self):
        return self.isStill
    
    def is_empty(self):
        return np.sum(self.current_state) == 0
            

class GameOfLife(CellularAutomata):
    pass
    
    def update_cell_states(self):        
        self.next_state = self.current_state.copy()
        for y in range(self.numRows):
            for x in range(self.numCols):
                living_neighbors = self.get_nearby_neighbors(y, x)
                
                if self.current_state[y,x] == 0:
                    if living_neighbors == 3:
                        self.next_state[y,x] = 1
                    else:
                        self.next_state[y,x] = 0
                        
                elif self.current_state[y,x] == 1:
                    if living_neighbors == 2 or living_neighbors == 3:
                        self.next_state[y,x] = 1
                    else:
                        self.next_state[y,x] = 0
                        
        self.check_stillness()
                
        self.current_state = self.next_state
