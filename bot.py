import pygame
import random

class Bot():

    def __init__(self, img_size = None, img =pygame.image.load('img/bot.png')):
        self.row = 0
        self.column = 0
        self.banana_count = 0
        self.apple_count = 0
        self.watermelon_count = 0
        self.fruit_count = 0
        self.boardSize = 0
        if img_size: 
            img = pygame.transform.scale(img, (img_size, img_size))    
            self.img_size = img_size
        else:   
            self.img_size = img.get_size()[0]
        self.img = img
        self.path = list()
        
    def draw(self, new_frame, margin, width, height, grid_offset_x, grid_offset_y):
        full_width = margin + width
        full_height = margin + height
        new_frame.blit(self.img, ((full_width * self.column + margin + grid_offset_x + (full_width-self.img_size)/2), (full_height * self.row + margin + grid_offset_y+ (full_height-self.img_size)/2)))

    def move_up(self):
        if self.row - 1 >= 0:
            self.row -= 1

    def move_down(self):
        if self.row + 1 <= self.boardSize:
            self.row += 1

    def move_right(self):
        if self.column + 1 <= self.boardSize:
            self.column += 1

    def move_left(self):
        if self.column - 1 >= 0:
            self.column -= 1

    def move_to(self, pos):
        self.row = pos[0]
        self.column = pos[1]

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
        self.boardSize = size;

    def setPath(self, newPath):
        self.path = newPath;

    def hasPath(self):
        if len(self.path) > 0:
            return True;

    def nextPathMovement(self):
        self.move_to(self.path[0])
        self.path.pop(0)