from sense_hat import SenseHat
from cellular_automata import GameOfLife
from time import sleep
from random import randint
import random
import numpy as np

class SenseHatExtended():
    """
    This is a custom class that extends the functionality
    of the SenseHat library. If you want to access te sense object
    that is created usally from sense = SenseHat(), then for example:
    
    WITHOUT SenseHatExtendedFunctionality():
    sense = SenseHat()
    sense.set_pixel(...)
    
    WITH SenseHatExtendedFunctionality():
    sense_extended = SenseHatExtendedFunctionality()
    sense_extended.sense.set_pixel(...)
        OR
    self.sense.set_pixel(...)
    
    I can not inherit some of SenseHat's properties which is why I am
    not using inhertance. Instead, I am adding a sense = SenseHat() obejct
    as a property for the SenseHatExtendedFunctionality class.
    
    """

    default_animation_speed = .04 # used for the speed of animations.
    interval_animation_speed = .05
    numRows = 8
    numCols = 8
    life = None
    isPlaying = False
    
    def __init__(self):
        print("Sense Hat Extended Version Initialized!")
        self.sense = SenseHat() # Create new sense hat object.
        self.life = GameOfLife(self.numRows, self.numCols)
        
    def display_logo(self, animate = True):
        print("Display Logo!")
        self.sense.clear() # Clear grid before making changes.
        self.adjust_orientation() # Adjust orientation.
        
        if animate:
            animation_speed = self.default_animation_speed # Animation
        else:
            animation_speed = 0 # No animation
        
        # Colors based off RGB value:
        red = (255, 0, 0)
        green = (0, 255, 0)
        
        # 1st row:
        for i in range(3,5):
            self.sense.set_pixel(i, 1, green)
            sleep(animation_speed)
            
        # 2nd row:
        for i in range(2,6):
            self.sense.set_pixel(i, 2, green)
            sleep(animation_speed)
    
        # 3rd row:
        for i in range(2,6):
            self.sense.set_pixel(i, 3, red)
            sleep(animation_speed)
        
        # 4th row:
        for i in range(1,7):
            self.sense.set_pixel(i, 4, red)
            sleep(animation_speed)
            
        # 5th row:
        for i in range(2,6):
            self.sense.set_pixel(i, 5, red)
            sleep(animation_speed)
            
        # 6th row:
        for i in range(3,5):
            self.sense.set_pixel(i, 6, red)
            sleep(animation_speed)
            
        
    def display_random(self, animate = True):
        self.clear_matrix() # Clear grid before making any changes.
        self.adjust_orientation() # Adjust orientation.
        
        if animate:
            animation_speed = self.default_animation_speed
        else:
            animation_speed = 0
        
        for y in range(self.numRows):
            for x in range(self.numCols):
                random_color = self.get_random_color()
                self.sense.set_pixel(y, x, random_color)
                sleep(animation_speed)
                
    def get_random_color(self):
        random_red = randint(0, 255)
        random_green = randint(0, 255)
        random_blue = randint(0, 255)
        return (random_red, random_green, random_blue)
        
    def adjust_orientation(self):
        """For more info: https://bit.ly/3iG7QeA and jump
            to the 'Orientation' section that explains which
            way is up for the pi sensor hat."""
            
        acceleration = self.sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']

        x = round(x, 0)
        y = round(y, 0)
        z = round(z, 0)
        
        # Update the rotation of the display depending on which way up the Sense HAT is
        if x  == -1:
            self.sense.set_rotation(90)
        elif x ==1:
            self.sense.set_rotation(270)
        elif y == 1:
            self.sense.set_rotation(0)
        elif y == -1:
            self.sense.set_rotation(180)
        else:
            self.sense.set_rotation(180)
            
        
    def play_life(self, animation_update_delay = 0):
        # Start() function
        self.reset_life() # Clear and adjust orientation before updating.
        isPlaying = True
        
        # Update() function
        while isPlaying:
            if self.life.is_empty() or self.life.is_still():
                sleep(animation_update_delay)
                self.reset_life()
            
            self.life.update_cell_states()
            self.update_matrix_colors_from_cell_states()
            sleep(animation_update_delay)
    
    def update_matrix_colors_from_cell_states(self, animation_delay = 0):
        alive_color = self.life.alive
        dead_color = self.life.dead
        
        for y in range(self.numRows):
            for x in range(self.numCols):
                if self.life.current_state[y,x] == 1:
                    self.sense.set_pixel(x, y, alive_color)
                elif self.life.current_state[y,x] == 0:
                    self.sense.set_pixel(x, y, dead_color)
        
                sleep(animation_delay)
    
    def reset_life(self):
        self.sense.clear()
        self.adjust_orientation()
        self.life.clear_cell_states()
        self.life.randomize_cell_states()
        self.update_matrix_colors_from_cell_states(self.interval_animation_speed)
        
pi = SenseHatExtended()
sleep(5)
pi.play_life(.1)