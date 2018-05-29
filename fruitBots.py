import pygame
from bot import Bot
from slidersFile import Slider
import random
import numpy as np
import itertools
import pathFinding
import GUI
from GUI import SlideBar, Button

# widow size
WINDOW_SIZE = [1240, 640]

# grid size

GRID_SIZE_SMALL = 5
GRID_SIZE_MEDIUM = 8
GRID_SIZE_LARGE = 12

grid_size = GRID_SIZE_MEDIUM

grid_total_width = grid_total_height = 420
cell_margin = 2

cell_width = cell_height = (grid_total_width- (cell_margin*grid_size))//grid_size

icon_size = 30

# create grid
grid = np.array([[0 for x in range(grid_size)] for y in range(grid_size)])

graph = pathFinding.Graph()
graph.constructGraphFromGrid(grid_size)

# variavel de controlo do ciclo principal
end = False

# bot
player1 = Bot(icon_size, pygame.image.load('img/walle.png'))
player1.setBoard_size(grid_size)

player2 = Bot(icon_size, pygame.image.load('img/eve.png'))
player2.setBoard_size(grid_size)

game_start = False
steps = 0

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)

# nova imagem a mostrar
new_frame = None

clock = pygame.time.Clock()
pygame.display.set_caption("Fruit Bots")

WHITE = (255, 255, 255)
DARK_GREY = (30, 34, 38)
GREY = (52, 56, 60)
LIGHT_GREY = (171, 178, 186)

TURQUOISE = (1, 174, 180)
LIGHT_TURQUOISE = (167, 221, 223)
DARK_TURQUOISE = (14, 92, 104)

ORANGE = (209, 112, 31)
LIGHT_ORANGE = (249, 209, 147)
DARK_ORANGE = (151, 51, 0)

screen.fill(GREY)

logo = pygame.image.load("img/logo_watermelon.png")
# logo = pygame.transform.scale(logo, (banner_base_size, banner_base_size))
banana_img  = pygame.image.load('img/banana3.png')
banana_img = pygame.transform.scale(banana_img, (icon_size, icon_size))

apple_img = pygame.image.load('img/apple.png')
apple_img = pygame.transform.scale(apple_img, (icon_size, icon_size))

watermelon_img = pygame.image.load('img/watermelon.png')
watermelon_img = pygame.transform.scale(watermelon_img, (icon_size, icon_size))

banner_base_size = 65
grid_offset_x = 10
grid_offset_y = 75

bot_menu_width = 300
bot_menu_margin = 50

font_title_size = 20
font_title = pygame.font.Font("font/Roboto-Regular.ttf", font_title_size)

font_menu_size = 14
font_menu = pygame.font.Font("font/Roboto-Regular.ttf", font_menu_size)

# for random actions
last_action_time = pygame.time.get_ticks()

BANANA = 1
APPLE = 2
WATERMELON = 3

total_bananas = num_bananas = 2
total_apples = num_apples = 2
total_watermelons = num_watermelons = 2

total_fruits = num_fruits = num_bananas + num_apples + num_watermelons

pairs = list(itertools.product(np.arange(grid_size), repeat=2))
del pairs[0]
del pairs[len(pairs)-1]

positions = list()

###########################################################################

def process_pygame_events():
    global game_start
    global end
    global start_time
    global time_left
    global last_action_time

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if not game_start:
                if mouse in sb_apple:
                    sb_apple.focus()
                elif mouse in sb_banana:
                    sb_banana.focus()
                elif mouse in sb_watermelon:
                    sb_watermelon.focus()
                elif mouse in bt_shuffle:
                    bt_shuffle.click()
                elif mouse in bt_board_small and grid_size != GRID_SIZE_SMALL:
                    bt_board_small.click()
                elif mouse in bt_board_medium and grid_size != GRID_SIZE_MEDIUM:
                    bt_board_medium.click()
                elif mouse in bt_board_large and grid_size != GRID_SIZE_LARGE:
                    bt_board_large.click()

        elif event.type == pygame.MOUSEBUTTONUP:
                sb_banana.unfocus()
                sb_apple.unfocus()
                sb_watermelon.unfocus()
                bt_shuffle.release()
                bt_board_small.release()
                bt_board_medium.release()
                bt_board_large.release()
        else:

            if mouse in bt_shuffle and not game_start:
                bt_shuffle.color = LIGHT_ORANGE
            else:
                bt_shuffle.color = ORANGE

            if mouse in bt_board_small and not game_start:
                bt_board_small.color = LIGHT_TURQUOISE
            elif grid_size == GRID_SIZE_SMALL:
                bt_board_small.color = DARK_TURQUOISE
            else:
                bt_board_small.color = TURQUOISE

            if mouse in bt_board_medium and not game_start:
                bt_board_medium.color = LIGHT_TURQUOISE
            elif grid_size == GRID_SIZE_MEDIUM:
                bt_board_medium.color = DARK_TURQUOISE
            else:
                bt_board_medium.color = TURQUOISE

            if mouse in bt_board_large and not game_start:
                bt_board_large.color = LIGHT_TURQUOISE
            elif grid_size == GRID_SIZE_LARGE:
                bt_board_large.color = DARK_TURQUOISE
            else:
                bt_board_large.color = TURQUOISE

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_SPACE]:
            print("PRESS SPACE")
            if not game_start:
                game_start = True


def draw_banner():
    global new_frame
    global steps

    new_frame.fill(DARK_GREY, (0, 0, banner_base_size, banner_base_size))
    new_frame.fill(GREY, (banner_base_size, 0, WINDOW_SIZE[0] - banner_base_size, banner_base_size))

    new_frame.blit(logo, (0, 0, 50, 50))

    title = font_title.render("FruitBots", 1, LIGHT_GREY)
    new_frame.blit(title, (font_title_size + banner_base_size, banner_base_size // 2 - (font_title_size // 2)))

    text = font_title.render("Steps: " + str(steps), 1, LIGHT_GREY)
    new_frame.blit(text, (
        WINDOW_SIZE[0] - text.get_width() - font_title_size, banner_base_size // 2 - (font_title_size // 2)))

def remove_old_fruits(fruit_type, old_total_fruits):

    global grid
    global total_fruits
    global pairs

    n_fruits_remove = old_total_fruits - total_fruits

    old_positions = pairs[:old_total_fruits]

    print(grid)
    print(fruit_type)

    match_fruits = np.asarray(np.where(grid == fruit_type)).T
    match_fruits = [tuple(l) for l in match_fruits]
    print("march_fruits", match_fruits)
    
    random.shuffle(match_fruits)
    fruit_delete = match_fruits[:n_fruits_remove]

    for f in fruit_delete:
        grid[f[0]][f[1]] = 0
        pairs.remove(f)
        pairs.append(f)

def add_new_fruits(fruit_type, old_total_fruits):

    global pairs
    global grid
    global total_fruits
    global positions

    positions = pairs[old_total_fruits:total_fruits]

    for i in range(len(positions)):
        pos = positions[i]
        grid[pos[0]][pos[1]] = fruit_type

def place_fruits(randomize):

    global grid
    global total_fruits
    global total_bananas
    global total_apples
    global total_watermelons
    global pairs
    global positions

    # place fruits

    # shuffle possible positions
    if(randomize): random.shuffle(pairs)
    positions = pairs[:total_fruits]

    bananas_placed = 0
    apples_placed = 0
    watermelons_placed = 0
    for i in range(total_fruits):
        pos = positions[i]
        if bananas_placed < total_bananas:
            to_place = BANANA
            bananas_placed += 1
        elif apples_placed < total_apples:
            to_place = APPLE
            apples_placed += 1
        elif watermelons_placed < total_watermelons:
            to_place = WATERMELON
            watermelons_placed += 1

        grid[pos[0]][pos[1]] = to_place

def draw_grid():
    global new_frame
    global grid
    global grid_size
    global cell_width
    global cell_height

    #print("grid", grid)

    grid_copy = grid.copy()

    for row in range(0, len(grid_copy)):
        for column in range(0, len(grid_copy)):
            
            full_width = cell_margin + cell_width
            full_height = cell_margin + cell_height

            pygame.draw.rect(new_frame, LIGHT_GREY,
                             [full_width * column + grid_offset_x + cell_margin, full_height * row + grid_offset_y + cell_margin,
                              cell_width, cell_height], 1)

            fruit_to_draw = None
            # draw fruits
            if grid_copy[row][column] == BANANA:
                fruit_to_draw = banana_img
            elif grid_copy[row][column] == APPLE:
                fruit_to_draw = apple_img
            elif grid_copy[row][column] == WATERMELON:
                fruit_to_draw = watermelon_img

            if fruit_to_draw:
                new_frame.blit(fruit_to_draw, (
                    (full_width * column + cell_margin + grid_offset_x + (full_width - icon_size) / 2),
                    (full_height * row + cell_margin + grid_offset_y + (full_height - icon_size) / 2)))


def draw_botmenu(bot, number):

    global new_frame

    x = grid_offset_x + grid_total_width + bot_menu_margin

    menu_h = (grid_total_height//2)-banner_base_size-grid_offset_x- (grid_offset_x/2)
    y = grid_offset_y + cell_margin
    y = y + (menu_h+banner_base_size+grid_offset_x*2 if number == 2 else 0)

    bot_img = bot.get_img()
    bot_img_h = bot_img.get_size()[1]

    pygame.draw.rect(new_frame, LIGHT_GREY,(x, y,
                              bot_menu_width, banner_base_size), 1)

    pygame.draw.rect(new_frame, LIGHT_GREY,(x, banner_base_size+ y + grid_offset_x,
                              bot_menu_width, menu_h), 1)

    new_frame.blit(bot_img, (
        x+grid_offset_x, y+((banner_base_size) // 2 - (bot_img_h // 2))))

    text = font_title.render("Bot "+str(number), 1, LIGHT_GREY)
    
    new_frame.blit(text, (
        x+(grid_offset_x*2) + bot_img_h, y+((banner_base_size) // 2 - (font_title_size // 2))))


def draw_buttons():
    global new_frame

    text_board_size = font_menu.render("Board Size", 1, DARK_GREY)
    new_frame.blit(text_board_size, (bt_x_ori+bt_board_size[0]*2+ grid_offset_x, bt_y- bt_board_size[1]))

    bt_board_small.render(new_frame)
    bt_board_medium.render(new_frame)
    bt_board_large.render(new_frame)
    bt_shuffle.render(new_frame)

def draw_slidebars():
    global new_frame

    x = grid_offset_x + (sb_margin//2)
    y = sb_y - (icon_size) - sb_size[1]
    text_margin = 5

    new_frame.blit(banana_img, (x, y))
    text_banana = font_menu.render("Bananas", 1, DARK_GREY)
    new_frame.blit(text_banana, (x+icon_size+text_margin, y+(font_menu_size//2)))

    sb_banana.render(new_frame)

    x += sb_size[0] + sb_margin
    new_frame.blit(apple_img, (x, y))
    text_apple = font_menu.render("Apples", 1, DARK_GREY)
    new_frame.blit(text_apple, (x+icon_size+text_margin, y+(font_menu_size//2)))

    sb_apple.render(new_frame)
    
    x += sb_size[0] + sb_margin
    new_frame.blit(watermelon_img, (x, y))
    text_watermelon = font_menu.render("Watermelons", 1, DARK_GREY)
    new_frame.blit(text_watermelon, (x+icon_size+text_margin, y+(font_menu_size//2)))

    sb_watermelon.render(new_frame)

def game_loop():
    global new_frame
    global game_start
    global last_action_time
    global num_fruits
    global num_bananas
    global num_apples
    global num_watermelons
    global positions
    global steps
    global cell_width
    global cell_height
    global grid

    new_frame = pygame.Surface([WINDOW_SIZE[0],WINDOW_SIZE[1]])
    new_frame.fill(WHITE)

    draw_banner()

    draw_grid()
    draw_botmenu(player1, 1)
    draw_botmenu(player2, 2)

    if game_start:
        # new action - random - every second
        time_elapsed_since_last_action = pygame.time.get_ticks() - last_action_time
        if time_elapsed_since_last_action >= 500:
            print(time_elapsed_since_last_action)
            grid[player1.row][player1.column] = 0
            grid[player2.row][player2.column] = 0
            steps += 1
           
            if not player1.hasPath() and num_fruits > 0: #TODO Make bot look for most desired fruit not the first of the list
                fruit = positions[0]
                positions.pop(0)
                startNode = str(player1.row)+str(player1.column)
                endNode = str(fruit[0])+str(fruit[1])
                movement = graph.getPathForMovement(graph.bfs_short_path(startNode, endNode))
                player1.setPath(movement)

            player1.nextPathMovement()
            
            #player1.do_random_action()
            last_action_time = pygame.time.get_ticks()

        if grid[player1.row][player1.column] == BANANA:
            player1.catch_banana()
            grid[player1.row][player1.column] = -1
            num_fruits -= 1
            num_bananas -= 1
        elif grid[player1.row][player1.column] == APPLE:
            player1.catch_apple()
            grid[player1.row][player1.column] = -1
            num_fruits -= 1
            num_apples -= 1
        elif grid[player1.row][player1.column] == WATERMELON:
            player1.catch_watermelon()
            grid[player1.row][player1.column] = -1
            num_fruits -= 1
            num_watermelons -= 1

        if grid[player2.row][player2.column] == BANANA:
            player2.catch_banana()
            grid[player2.row][player2.column] = -1
            num_fruits -= 1
            num_bananas -= 1
        elif grid[player2.row][player2.column] == APPLE:
            player2.catch_apple()
            grid[player2.row][player2.column] = -1
            num_fruits -= 1
            num_apples -= 1
        elif grid[player2.row][player2.column] == WATERMELON:
            player2.catch_watermelon()
            grid[player2.row][player2.column] = -1
            num_fruits -= 1
            num_watermelons -= 1

        if num_fruits == 0:
            print("here")
            print(num_fruits)
            game_start = False
            new_game()

    player1.draw(new_frame, cell_margin, cell_width, cell_height, grid_offset_x, grid_offset_y)

    player2.draw(new_frame, cell_margin, cell_width, cell_height, grid_offset_x, grid_offset_y)

    draw_slidebars()
    draw_buttons()

def new_game(place = True):
    global steps
    global last_action_time
    global grid
    global grid_size
    global num_fruits
    global total_fruits
    global total_watermelons
    global total_apples
    global total_bananas

    steps = 0
    last_action_time = pygame.time.get_ticks()

    grid = np.array([[0 for x in range(grid_size)] for y in range(grid_size)])
    player1.row = player1.column = 0
    player2.row = player2.column = grid_size-1
    grid[player1.row][player1.column] = -1
    grid[player2.row][player2.column] = -2

    if place: place_fruits(False)

    num_bananas = total_bananas
    num_apples = total_apples
    num_watermelons = total_watermelons

    player1.banana_count = player1.apple_count = player1.watermelon_count = player1.fruit_count = 0
    player2.banana_count = player2.apple_count = player2.watermelon_count = player2.fruit_count = 0

    total_fruits = num_fruits = num_bananas + num_apples + num_watermelons

    print(grid)

###########################################################################

#
# Buttons
#

def func_shuffle():
    global grid
    global grid_size

    grid = np.array([[0 for x in range(grid_size)] for y in range(grid_size)])
    player1.row = player1.column = 0
    player2.row = player2.column = grid_size-1
    grid[player1.row][player1.column] = -1
    grid[player2.row][player2.column] = -2

    place_fruits(True)

def set_board_size(new_size):
    global grid
    global grid_size
    global cell_width
    global cell_height
    global pairs

    grid_size = new_size
    cell_width = cell_height = (grid_total_width- (cell_margin*grid_size))//grid_size

    # create grid
    grid = np.array([[0 for x in range(grid_size)] for y in range(grid_size)])

    player1.row = player1.column = 0
    player2.row = player2.column = grid_size-1
    grid[player1.row][player1.column] = -1
    grid[player2.row][player2.column] = -2
    player1.setBoard_size(grid_size)
    player2.setBoard_size(grid_size)

    print(grid)

    pairs = list(itertools.product(np.arange(grid_size), repeat=2))
    del pairs[0]
    del pairs[len(pairs)-1]

    place_fruits(True)

def func_board_small():

    set_board_size(GRID_SIZE_SMALL)

def func_board_medium():

    set_board_size(GRID_SIZE_MEDIUM)

def func_board_large():
    set_board_size(GRID_SIZE_LARGE)    

bt_margin = 15
bt_shuffle_size = (130,40)

bt_x_ori=bt_x = grid_offset_x + grid_total_width + bot_menu_margin + (bt_shuffle_size[0]//2)
bt_y = 560

bt_shuffle = Button(func_shuffle, (bt_x, bt_y), bt_shuffle_size, 'Shuffle Board', color = ORANGE)

bt_x += (bt_shuffle_size[0]//2) + bt_margin*3
bt_board_size = (40,40)
bt_board_small = Button(func_board_small, (bt_x, bt_y), bt_board_size, 'S', color = TURQUOISE)

bt_x += bt_board_size[0] + bt_margin
bt_board_medium = Button(func_board_medium, (bt_x, bt_y), bt_board_size, 'M', color = TURQUOISE)

bt_x += bt_board_size[0] + bt_margin
bt_board_large = Button(func_board_large, (bt_x, bt_y), bt_board_size, 'L', color = TURQUOISE)

#
# Sliders settings
#

sb_margin = 25
print(grid_total_width)
print(grid_total_width//3 -(sb_margin*2))
sb_size = (grid_total_width//3 -(sb_margin),30)

sb_x = sb_x_init = grid_offset_x + sb_size[0]//2 + (sb_margin//2)
sb_y = 580

# bananas
sb_banana = SlideBar(print, (sb_x, sb_y), sb_size, 0, 5, 1, interval=4)

sb_banana.set(total_bananas)
def func_sb_banana(value):
    global total_fruits
    global total_bananas
    old_total_fruits = total_fruits
    total_fruits = total_fruits - total_bananas + value
    if (total_fruits == 0): 
        total_fruits = old_total_fruits
        sb_banana.set(total_bananas)
        return
    total_bananas = value

    if total_fruits > old_total_fruits: add_new_fruits(BANANA, old_total_fruits)
    else: remove_old_fruits(BANANA, old_total_fruits)

sb_banana.func = func_sb_banana

# apples
sb_x += sb_size[0] + sb_margin
sb_apple = SlideBar(print, (sb_x, sb_y), sb_size, 0, 5, 1, interval=4)

sb_apple.set(total_apples)
def func_sb_apple(value):
    global total_fruits
    global total_apples

    old_total_fruits = total_fruits
    total_fruits = total_fruits - total_apples + value
    if (total_fruits == 0): 
        total_fruits = old_total_fruits
        sb_apple.set(total_apples)
        return
    total_apples = value

    if total_fruits > old_total_fruits: add_new_fruits(APPLE, old_total_fruits)
    else: remove_old_fruits(APPLE, old_total_fruits)

sb_apple.func = func_sb_apple

# watermelons
sb_x += sb_size[0] + sb_margin
sb_watermelon = SlideBar(print, (sb_x, sb_y), sb_size, 0, 5, 1, interval=4)

sb_watermelon.set(total_watermelons)
def func_sb_watermelon(value):
    global total_fruits
    global total_watermelons

    old_total_fruits = total_fruits
    total_fruits = total_fruits - total_watermelons + value
    if (total_fruits == 0): 
        total_fruits = old_total_fruits
        sb_watermelon.set(total_watermelons)
        return
    total_watermelons = value

    if total_fruits > old_total_fruits: add_new_fruits(WATERMELON, old_total_fruits)
    else: remove_old_fruits(WATERMELON, old_total_fruits)

sb_watermelon.func = func_sb_watermelon


new_game(False)
place_fruits(True)
while not end:
    process_pygame_events()

    game_loop()

    # actualizar pygame com a nova imagem
    screen.blit(new_frame, (0, 0))
    pygame.display.update()

pygame.quit()
quit()
