import pygame
import random

BANANA = 0
APPLE = 1
WATERMELON = 2

class Bot():

    def __init__(self, img_size=None, img=pygame.image.load('img/bot.png')):
        self.row = 0
        self.column = 0
        self.banana_count = 0
        self.apple_count = 0
        self.watermelon_count = 0
        self.fruit_count = 0
        self.fruits_left = 0
        self.bananas_left = 0
        self.apples_left = 0
        self.watermelons_left = 0
        self.fruit_pos = {}
        self.bananas_pos = {}
        self.apples_pos = {}
        self.watermelons_pos = {}
        self.time = 0
        self.Intentions = {}
        if img_size:
            img = pygame.transform.scale(img, (img_size, img_size))
            self.img_size = img_size
        else:
            self.img_size = img.get_size()[0]
        self.img = img
        self.boardSize = 0
        self.path = list()

    def draw(self, new_frame, margin, width, height, grid_offset_x, grid_offset_y):
        full_width = margin + width
        full_height = margin + height
        new_frame.blit(self.img, (
        (full_width * self.column + margin + grid_offset_x + (full_width - self.img_size) / 2),
        (full_height * self.row + margin + grid_offset_y + (full_height - self.img_size) / 2)))

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

    '''def do_random_action(self):
         action = random.choice([self.move_down,self.move_left, self.move_right, self.move_up])
         action()'''

    def setBoard_size(self, size):
        self.boardSize = size

    def setPath(self, newPath):
        self.path = newPath

    def hasPath(self):
        if len(self.path) > 0:
            return True

    def nextPathMovement(self):
        self.move_to(self.path[0])
        self.path.pop(0)

    def updateTime(self, board_time):
        self.time = board_time

    def update_num_fruits(self, current_fruits_left):
        self.fruits_left = current_fruits_left[0]
        self.bananas_left = current_fruits_left[1]
        self.apples_left = current_fruits_left[2]
        self.watermelons_left = current_fruits_left[3]

    def set_fruits_pos(self, fruits_pos):
        self.fruit_pos = fruits_pos[0]
        self.bananas_pos = fruits_pos[1]
        self.apples_pos = fruits_pos[2]
        self.watermelons_pos = fruits_pos[3]

    def set_initial_intention(self, intention):
        self.Intentions.append(intention)

    def brf(self, perceptions):  # perceptions have different types of variables - list{int, list, list}
        self.updateTime(perceptions[0])
        if self.fruits_left > perceptions[1][0]:
            self.update_num_fruits(perceptions[1])
            self.set_fruits_pos(perceptions[2])

    def options(self, belief_list, intentions):  # TODO function that generates Bot's desires
        return

    def filter(self, belief_list, desires, intentions):  # TODO function that selects best options for Bot to commit
        return

    def plan(self, belief_list, intentions):  # TODO function that defines Bot's plan
        return

    def empty(self, plan):  # TODO verify if plan stack is empty
        return

    def succeeded(self, intentions, belief_list):  # TODO verify if intentions have succeeded
        return

    def impossible(self, intentions, belief_list):  # TODO verify if intentions are impossible
        return

    def reconsider(self, intentions, belief_list):  # TODO control function that decides when to reconsider intentions
        return

    def sound(self, intentions, belief_list):  # TODO control function that decides when to reconsider plan !NOT SURE!
        return
