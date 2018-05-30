import pygame
import math
import random
import pathFinding
from react.react import React

BANANA = 0
APPLE = 1
WATERMELON = 2

# actions
CATCH_UP = 0
CATCH_LEFT = 1
CATCH_DOWN = 2
CATCH_RIGHT = 3
MOVE_UP = 4
MOVE_LEFT = 5
MOVE_DOWN = 6
MOVE_RIGHT = 7

class Bot():

    def __init__(self, symbol, img_size=None, img=pygame.image.load('img/bot.png')):
        self.row = 0
        self.col = 0
        self.symbol = symbol
        self.banana_count = 0
        self.apple_count = 0
        self.watermelon_count = 0
        self.fruit_count = 0
        
        if img_size:
            img = pygame.transform.scale(img, (img_size, img_size))
            self.img_size = img_size
        else:
            self.img_size = img.get_size()[0]

        self.img = img
        self.boardSize = 0
        self.architecture = React()

    def symbol(self):
        print("self", self.symbol)
        return self.symbol

    def set_architecture(self, new_architecture):
        self.architecture = new_architecture

    def get_img(self):
        return self.img

    def draw(self, new_frame, margin, width, height, grid_offset_x, grid_offset_y):
        full_width = margin + width
        full_height = margin + height
        new_frame.blit(self.img, (
        (full_width * self.col + margin + grid_offset_x + (full_width - self.img_size) / 2),
        (full_height * self.row + margin + grid_offset_y + (full_height - self.img_size) / 2)))

    def move_up(self):
        if self.row - 1 >= 0:
            self.row -= 1

    def move_down(self):
        if self.row + 1 < self.boardSize:
            self.row += 1

    def move_right(self):
        if self.col + 1 < self.boardSize:
            self.col += 1

    def move_left(self):
        if self.col - 1 >= 0:
            self.col -= 1

    def move_to(self, pos):
        self.row = pos[0]
        self.col = pos[1]

    def catch_banana(self):
        self.banana_count += 1
        self.fruit_count += 1

    def catch_apple(self):
        self.apple_count += 1
        self.fruit_count += 1

    def catch_watermelon(self):
        self.watermelon_count += 1
        self.fruit_count += 1

    def do_random_action(self):
         action = random.choice([self.move_down,self.move_left, self.move_right, self.move_up])
         action()

    def setBoard_size(self, size):
        self.boardSize = size

    def get_fruit_pos(self, action):
        if action == CATCH_UP:
            fruit_pos = (self.row-1, self.col)
        elif action == CATCH_LEFT:
            fruit_pos = (self.row, self.col-1)
        elif action == CATCH_DOWN:
            fruit_pos = (self.row+1, self.col)
        elif action == CATCH_RIGHT:
            fruit_pos = (self.row, self.col+1)

        return fruit_pos

    # return action executed and, if action = move: new position, if action=catch: fruit position 
    def execute(self, perception):

        action = self.architecture.execute(perception)
        
        if action >= MOVE_UP:
            if action == MOVE_UP: self.move_up()
            elif action == MOVE_DOWN: self.move_down()
            elif action == MOVE_LEFT: self.move_left()
            elif action == MOVE_RIGHT: self.move_right()
            cell_pos=(self.row,self.col)
        else: 
            cell_type = perception[action]
            if cell_type == BANANA: self.catch_banana()
            elif cell_type == APPLE: self.catch_apple()
            elif cell_type == WATERMELON: self.catch_watermelon()
            cell_pos= self.get_fruit_pos(action)

        return (action, cell_pos)

    def get_architecture(self):
        return self.architecture.__class__.__name__